from config import supabase

class StudentEvents:
    @staticmethod
    def get_active_events():
        """Fetch all active events (includes upcoming and ongoing) with department information"""
        try:
            events = supabase.table("events").select(
                "*, users!events_department_id_fkey(full_name, department_name, email, role)"
            ).eq("status", "Active").order("date", desc=False).execute()
            return events
        except Exception as e:
            print(f"Error fetching active events: {e}")
            return None

    @staticmethod
    def get_event_by_id(event_id):
        """Get specific event details"""
        try:
            event = supabase.table("events").select(
                "*, users!events_department_id_fkey(full_name, department_name, email, role)"
            ).eq("id", event_id).execute()
            return event
        except Exception as e:
            print(f"Error fetching event by ID: {e}")
            return None

    @staticmethod
    def get_available_seats(event_id):
        """Calculate remaining seats for limited-seat events"""
        try:
            # Get event details
            event_response = supabase.table("events").select("participant_limit").eq("id", event_id).execute()
            
            if not event_response.data:
                return 0
            
            event = event_response.data[0]
            participant_limit = event.get("participant_limit")
            
            # If no limit, return -1 to indicate unlimited
            if participant_limit is None:
                return -1
            
            # Count approved registrations
            registrations_response = supabase.table("registrations").select("id").eq("event_id", event_id).eq("registration_status", "Approved").execute()
            
            approved_count = len(registrations_response.data) if registrations_response.data else 0
            
            # Calculate remaining seats
            remaining = participant_limit - approved_count
            return max(0, remaining)  # Ensure non-negative
            
        except Exception as e:
            print(f"Error calculating available seats: {e}")
            return 0

    @staticmethod
    def is_free_for_all(event_id):
        """Check if event is free-for-all (no participant limit)"""
        try:
            event_response = supabase.table("events").select("participant_limit").eq("id", event_id).execute()
            
            if not event_response.data:
                return False
            
            event = event_response.data[0]
            # Free-for-all events have NULL participant_limit
            return event.get("participant_limit") is None
            
        except Exception as e:
            print(f"Error checking event type: {e}")
            return False

    @staticmethod
    def is_limited_seat(event_id):
        """Check if event has limited seats"""
        try:
            event_response = supabase.table("events").select("participant_limit").eq("id", event_id).execute()
            
            if not event_response.data:
                return False
            
            event = event_response.data[0]
            participant_limit = event.get("participant_limit")
            
            # Limited-seat events have a non-null participant_limit
            return participant_limit is not None and participant_limit > 0
            
        except Exception as e:
            print(f"Error checking event type: {e}")
            return False

    @staticmethod
    def is_event_full(event_id):
        """Check if a limited-seat event is full"""
        try:
            available_seats = StudentEvents.get_available_seats(event_id)
            
            # If available_seats is -1, it's unlimited (free-for-all)
            if available_seats == -1:
                return False
            
            # Event is full if no seats remaining
            return available_seats <= 0
            
        except Exception as e:
            print(f"Error checking if event is full: {e}")
            return True  # Assume full on error for safety
