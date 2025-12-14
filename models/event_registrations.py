from config import supabase
import uuid
import qrcode
from io import BytesIO
import base64

class EventRegistrations:
    @staticmethod
    def get_department_events(department_id):
        """Get all approved events for a department that have registrations"""
        # Get approved events that belong to this department
        events = supabase.table("events").select("*").eq("department_id", department_id).eq("status", "Active").order("date", desc=False).execute()
        return events

    @staticmethod
    def get_all_department_events(department_id):
        """Get all events for a department (including cancelled)"""
        events = supabase.table("events").select("*").eq("department_id", department_id).order("date", desc=False).execute()
        return events

    @staticmethod
    def get_registrations_by_event(event_id):
        """Get all registrations for a specific event with student details"""
        # Join registrations with users table to get student information
        registrations = supabase.table("registrations").select(
            "*, users!registrations_student_id_fkey(full_name, student_id, email)"
        ).eq("event_id", event_id).order("created_at", desc=True).execute()
        return registrations

    @staticmethod
    def get_registration_counts_by_event(event_id):
        """Get count of registrations by status for an event"""
        registrations = supabase.table("registrations").select("registration_status").eq("event_id", event_id).execute()
        
        counts = {"Pending": 0, "Approved": 0, "Rejected": 0}
        if registrations.data:
            for reg in registrations.data:
                status = reg.get("registration_status", "Pending")
                counts[status] = counts.get(status, 0) + 1
        
        return counts

    @staticmethod
    def approve_registration(registration_id):
        """Approve a registration and generate QR code"""
        try:
            # Generate unique code
            unique_code = str(uuid.uuid4())
            
            # Generate QR code image
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(unique_code)
            qr.make(fit=True)
            
            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert image to base64 string (for storage or display)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Update registration with approved status, unique code, and approval timestamp
            result = supabase.table("registrations").update({
                "registration_status": "Approved",
                "unique_code": unique_code,
                "approved_at": "now()"
            }).eq("id", registration_id).execute()
            
            return result
        except Exception as e:
            print(f"Error approving registration: {e}")
            return None

    @staticmethod
    def reject_registration(registration_id):
        """Reject a registration"""
        return supabase.table("registrations").update({
            "registration_status": "Rejected",
            "unique_code": None,
            "rejected_at": "now()"
        }).eq("id", registration_id).execute()

    @staticmethod
    def get_registration_by_id(registration_id):
        """Get a specific registration"""
        return supabase.table("registrations").select("*").eq("id", registration_id).execute()

    @staticmethod
    def get_event_details(event_id):
        """Get event details with department information"""
        return supabase.table("events").select(
            "*, users!events_department_id_fkey(full_name, department_name)"
        ).eq("id", event_id).execute()

    @staticmethod
    def check_event_belongs_to_department(event_id, department_id):
        """Verify that an event belongs to a specific department"""
        event = supabase.table("events").select("department_id").eq("id", event_id).execute()
        if event.data and len(event.data) > 0:
            return event.data[0]["department_id"] == department_id
        return False

    @staticmethod
    def cancel_event(event_id, department_id=None):
        """
        Cancel an event (change status to Cancelled)
        If department_id is provided, verify ownership
        """
        try:
            # If department_id provided, check ownership
            if department_id:
                if not EventRegistrations.check_event_belongs_to_department(event_id, department_id):
                    return False, "You don't have permission to cancel this event."
            
            # Check if event is already cancelled or completed
            event = supabase.table("events").select("status").eq("id", event_id).execute()
            if event.data:
                current_status = event.data[0]["status"]
                if current_status == "Cancelled":
                    return False, "Event is already cancelled."
                if current_status == "Completed":
                    return False, "Cannot cancel a completed event."
            
            # Update event status to Cancelled
            result = supabase.table("events").update({
                "status": "Cancelled"
            }).eq("id", event_id).execute()
            
            return True, "Event cancelled successfully."
        except Exception as e:
            return False, f"Error cancelling event: {str(e)}"

    @staticmethod
    def get_event_by_id(event_id):
        """Get event by ID"""
        return supabase.table("events").select("*").eq("id", event_id).execute()