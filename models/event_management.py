from config import supabase
from datetime import datetime

class EventManagement:
    @staticmethod
    def get_all_events():
        """Get all events with department information"""
        events = supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name, email, role)"
        ).order("date", desc=False).execute()
        return events

    @staticmethod
    def get_active_events():
        """Get only active events"""
        events = supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name, email, role)"
        ).eq("status", "Active").order("date", desc=False).execute()
        return events

    @staticmethod
    def get_event_by_id(event_id):
        """Get event details"""
        return supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name, email, role)"
        ).eq("id", event_id).execute()

    @staticmethod
    def cancel_event(event_id):
        """Cancel an event (OSAS can cancel any event)"""
        try:
            # Check if event exists and is not already cancelled
            event = supabase.table("events").select("status").eq("id", event_id).execute()
            
            if not event.data:
                return False, "Event not found."
            
            current_status = event.data[0]["status"]
            
            if current_status == "Cancelled":
                return False, "Event is already cancelled."
            
            if current_status == "Completed":
                return False, "Cannot cancel a completed event."
            
            # Update status to Cancelled
            supabase.table("events").update({
                "status": "Cancelled"
            }).eq("id", event_id).execute()
            
            return True, "Event cancelled successfully."
        except Exception as e:
            return False, f"Error cancelling event: {str(e)}"

    @staticmethod
    def check_schedule_conflict(location, date, start_time, end_time, exclude_event_id=None):
        """
        Check if there's a schedule conflict for the given location, date, and time
        Returns True if conflict exists, False otherwise
        """
        try:
            # Get all active events for the same date and location
            query = supabase.table("events").select("*").eq("location", location).eq("date", date).eq("status", "Active")
            
            existing_events = query.execute()
            
            if not existing_events.data:
                return False
            
            # Convert start_time and end_time to time objects for comparison
            if isinstance(start_time, str):
                new_start = datetime.strptime(start_time, "%H:%M:%S").time()
            else:
                new_start = start_time
                
            if isinstance(end_time, str):
                new_end = datetime.strptime(end_time, "%H:%M:%S").time()
            else:
                new_end = end_time
            
            # Check for time overlap with existing events
            for event in existing_events.data:
                # Skip if this is the same event being updated
                if exclude_event_id and event.get("id") == exclude_event_id:
                    continue
                
                # Convert existing event times
                if isinstance(event["start_time"], str):
                    existing_start = datetime.strptime(event["start_time"], "%H:%M:%S").time()
                else:
                    existing_start = event["start_time"]
                    
                if isinstance(event["end_time"], str):
                    existing_end = datetime.strptime(event["end_time"], "%H:%M:%S").time()
                else:
                    existing_end = event["end_time"]
                
                # Check for overlap: (StartA < EndB) and (EndA > StartB)
                if (new_start < existing_end) and (new_end > existing_start):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking schedule conflict: {e}")
            return True  # Assume conflict on error for safety

    @staticmethod
    def postpone_event(event_id, new_date, new_start_time, new_end_time):
        """
        Postpone/reschedule an event to a new date/time
        Returns (success: bool, message: str)
        """
        try:
            # Get current event details
            event_response = EventManagement.get_event_by_id(event_id)
            
            if not event_response.data:
                return False, "Event not found."
            
            event = event_response.data[0]
            
            # Check if event can be postponed
            if event["status"] == "Cancelled":
                return False, "Cannot postpone a cancelled event."
            
            if event["status"] == "Completed":
                return False, "Cannot postpone a completed event."
            
            # Check for schedule conflict with new date/time
            has_conflict = EventManagement.check_schedule_conflict(
                location=event["location"],
                date=new_date,
                start_time=new_start_time,
                end_time=new_end_time,
                exclude_event_id=event_id
            )
            
            if has_conflict:
                return False, "Schedule conflict detected with the new date/time. Please choose a different time."
            
            # Update event with new date/time
            supabase.table("events").update({
                "date": new_date,
                "start_time": new_start_time,
                "end_time": new_end_time
            }).eq("id", event_id).execute()
            
            return True, "Event postponed/rescheduled successfully!"
            
        except Exception as e:
            return False, f"Error postponing event: {str(e)}"

    @staticmethod
    def get_event_counts_by_status():
        """Get count of events grouped by status"""
        all_events = supabase.table("events").select("status").execute()
        
        counts = {"Active": 0, "Completed": 0, "Cancelled": 0}
        if all_events.data:
            for event in all_events.data:
                status = event.get("status", "Active")
                counts[status] = counts.get(status, 0) + 1
        
        return counts

    @staticmethod
    def get_events_by_department(department_id):
        """Get all events for a specific department"""
        events = supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name, email, role)"
        ).eq("department_id", department_id).order("date", desc=False).execute()
        return events

    @staticmethod
    def get_active_events_by_department(department_id):
        """Get only active events for a specific department"""
        events = supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name, email, role)"
        ).eq("department_id", department_id).eq("status", "Active").order("date", desc=False).execute()
        return events

    @staticmethod
    def get_event_counts_by_status_for_department(department_id):
        """Get count of events grouped by status for a specific department"""
        department_events = supabase.table("events").select("status, date, start_time, end_time").eq("department_id", department_id).execute()
        
        counts = {"Active": 0, "Ongoing": 0, "Completed": 0, "Cancelled": 0}
        
        if department_events.data:
            for event in department_events.data:
                display_status = EventManagement.get_event_display_status(event)
                counts[display_status] = counts.get(display_status, 0) + 1
        
        return counts
    
    @staticmethod
    def get_event_display_status(event):
        """Determine the display status of an event based on its date and time"""
        status = event.get("status", "Active")
        event_date_str = event.get("date")
        start_time_str = event.get("start_time")
        end_time_str = event.get("end_time")
        
        if status == "Active" and event_date_str and start_time_str and end_time_str:
            now = datetime.now()
            today = now.date()
            current_time = now.time()
            
            # Parse event date
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            
            # Parse event times
            if isinstance(start_time_str, str):
                start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            else:
                start_time = start_time_str
                
            if isinstance(end_time_str, str):
                end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
            else:
                end_time = end_time_str
            
            # Check if event is today
            if event_date == today:
                # Check if current time is within event time range
                if start_time <= current_time <= end_time:
                    return "Ongoing"
                elif current_time > end_time:
                    return "Completed"
                else:
                    return "Active"  # Event is today but hasn't started yet
            elif event_date < today:
                return "Completed"
        
        return status
    
    @staticmethod
    def update_event_status_if_needed(event_id, current_display_status):
        """Update the database status if it differs from the calculated display status"""
        try:
            # Only update if the display status is "Completed"
            if current_display_status == "Completed":
                # Get current database status
                event = supabase.table("events").select("status").eq("id", event_id).execute()
                
                if event.data and event.data[0]["status"] == "Active":
                    # Update to Completed
                    supabase.table("events").update({
                        "status": "Completed"
                    }).eq("id", event_id).execute()
                    return True
            return False
        except Exception as e:
            print(f"Error updating event status: {e}")
            return False
    
    @staticmethod
    def auto_update_completed_events():
        """Automatically update all Active events that should be Completed"""
        try:
            # Get all Active events
            active_events = supabase.table("events").select("*").eq("status", "Active").execute()
            
            if not active_events.data:
                return 0
            
            updated_count = 0
            for event in active_events.data:
                display_status = EventManagement.get_event_display_status(event)
                if display_status == "Completed":
                    if EventManagement.update_event_status_if_needed(event["id"], display_status):
                        updated_count += 1
            
            return updated_count
        except Exception as e:
            print(f"Error auto-updating events: {e}")
            return 0

    @staticmethod
    def cancel_department_event(event_id, department_id):
        """Cancel an event (only if it belongs to the department)"""
        try:
            # Check if event exists and belongs to the department
            event = supabase.table("events").select("status, department_id").eq("id", event_id).execute()
            
            if not event.data:
                return False, "Event not found."
            
            event_data = event.data[0]
            
            # Check if event belongs to the department
            if event_data["department_id"] != department_id:
                return False, "You can only manage events from your own department."
            
            current_status = event_data["status"]
            
            if current_status == "Cancelled":
                return False, "Event is already cancelled."
            
            if current_status == "Completed":
                return False, "Cannot cancel a completed event."
            
            # Update status to Cancelled
            supabase.table("events").update({
                "status": "Cancelled"
            }).eq("id", event_id).execute()
            
            return True, "Event cancelled successfully."
        except Exception as e:
            return False, f"Error cancelling event: {str(e)}"

    @staticmethod
    def postpone_department_event(event_id, department_id, new_date, new_start_time, new_end_time):
        """
        Postpone/reschedule an event (only if it belongs to the department)
        Returns (success: bool, message: str)
        """
        try:
            # Get current event details
            event_response = EventManagement.get_event_by_id(event_id)
            
            if not event_response.data:
                return False, "Event not found."
            
            event = event_response.data[0]
            
            # Check if event belongs to the department
            if event["department_id"] != department_id:
                return False, "You can only manage events from your own department."
            
            # Check if event can be postponed
            if event["status"] == "Cancelled":
                return False, "Cannot postpone a cancelled event."
            
            if event["status"] == "Completed":
                return False, "Cannot postpone a completed event."
            
            # Check for schedule conflict with new date/time
            has_conflict = EventManagement.check_schedule_conflict(
                location=event["location"],
                date=new_date,
                start_time=new_start_time,
                end_time=new_end_time,
                exclude_event_id=event_id
            )
            
            if has_conflict:
                return False, "Schedule conflict detected with the new date/time. Please choose a different time."
            
            # Update event with new date/time
            supabase.table("events").update({
                "date": new_date,
                "start_time": new_start_time,
                "end_time": new_end_time
            }).eq("id", event_id).execute()
            
            return True, "Event postponed/rescheduled successfully!"
            
        except Exception as e:
            return False, f"Error postponing event: {str(e)}"