from config import supabase
import uuid

class StudentRegistrations:
    @staticmethod
    def create_registration(student_id, event_id, auto_approve=False):
        """
        Create new registration (pending or approved based on event type)
        auto_approve=True for free-for-all events, False for limited-seat events
        """
        try:
            registration_data = {
                "student_id": student_id,
                "event_id": event_id,
                "registration_status": "Approved" if auto_approve else "Pending",
                "unique_code": None  # QR code will be generated upon approval for limited-seat events
            }
            
            result = supabase.table("registrations").insert(registration_data).execute()
            return result
            
        except Exception as e:
            print(f"Error creating registration: {e}")
            return None

    @staticmethod
    def get_student_registrations(student_id, status_filter=None):
        """
        Fetch all registrations for a student
        Optional status_filter: 'Pending', 'Approved', 'Rejected', or None for all
        """
        try:
            query = supabase.table("registrations").select(
                "*, events!registrations_event_id_fkey(*, users!events_department_id_fkey(full_name, department_name, role))"
            ).eq("student_id", student_id)
            
            # Apply status filter if provided
            if status_filter and status_filter != "All":
                query = query.eq("registration_status", status_filter)
            
            # Order by registration creation date (most recent first)
            # Note: Sorting by event date is done in the controller/template
            result = query.order("created_at", desc=True).execute()
            return result
            
        except Exception as e:
            print(f"Error fetching student registrations: {e}")
            return None

    @staticmethod
    def has_registered(student_id, event_id):
        """Check if student already registered for event"""
        try:
            result = supabase.table("registrations").select("id").eq("student_id", student_id).eq("event_id", event_id).execute()
            
            return result.data and len(result.data) > 0
            
        except Exception as e:
            print(f"Error checking registration: {e}")
            return False

    @staticmethod
    def cancel_registration(registration_id, student_id):
        """Cancel a pending registration (delete from database)"""
        try:
            # First verify the registration belongs to the student and is pending
            registration = supabase.table("registrations").select("registration_status, student_id").eq("id", registration_id).execute()
            
            if not registration.data:
                return False
            
            reg_data = registration.data[0]
            
            # Verify ownership
            if reg_data["student_id"] != student_id:
                return False
            
            # Only allow cancellation of pending registrations
            if reg_data["registration_status"] != "Pending":
                return False
            
            # Delete the registration
            supabase.table("registrations").delete().eq("id", registration_id).execute()
            return True
            
        except Exception as e:
            print(f"Error cancelling registration: {e}")
            return False

    @staticmethod
    def get_registration_with_qr(registration_id, student_id):
        """Get registration details including QR code"""
        try:
            result = supabase.table("registrations").select(
                "*, events!registrations_event_id_fkey(*, users!events_department_id_fkey(full_name, department_name, role))"
            ).eq("id", registration_id).eq("student_id", student_id).execute()
            
            return result
            
        except Exception as e:
            print(f"Error fetching registration with QR: {e}")
            return None

    @staticmethod
    def get_registration_counts(student_id):
        """Get count of registrations by status for a student"""
        try:
            result = supabase.table("registrations").select("registration_status").eq("student_id", student_id).execute()
            
            counts = {"Pending": 0, "Approved": 0, "Rejected": 0}
            
            if result.data:
                for reg in result.data:
                    status = reg.get("registration_status", "Pending")
                    counts[status] = counts.get(status, 0) + 1
            
            return counts
            
        except Exception as e:
            print(f"Error getting registration counts: {e}")
            return {"Pending": 0, "Approved": 0, "Rejected": 0}

    @staticmethod
    def get_registration_by_id(registration_id):
        """Get a specific registration by ID"""
        try:
            result = supabase.table("registrations").select(
                "*, events!registrations_event_id_fkey(*)"
            ).eq("id", registration_id).execute()
            
            return result
            
        except Exception as e:
            print(f"Error fetching registration: {e}")
            return None
