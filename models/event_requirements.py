from config import supabase

class EventRequirements:
    @staticmethod
    def add_requirement_to_event(event_id, requirement_name, description=None):
        """Add a requirement to an event"""
        try:
            result = supabase.table("event_requirements").insert({
                "event_id": event_id,
                "requirement_name": requirement_name,
                "description": description
            }).execute()
            return result
        except Exception as e:
            print(f"Error adding requirement: {e}")
            return None

    @staticmethod
    def get_event_requirements(event_id):
        """Get all requirements for an event"""
        try:
            result = supabase.table("event_requirements").select("*").eq("event_id", event_id).order("created_at", desc=False).execute()
            return result
        except Exception as e:
            print(f"Error fetching requirements: {e}")
            return None

    @staticmethod
    def delete_requirement(requirement_id):
        """Delete a requirement"""
        try:
            result = supabase.table("event_requirements").delete().eq("id", requirement_id).execute()
            return result
        except Exception as e:
            print(f"Error deleting requirement: {e}")
            return None

    @staticmethod
    def get_student_requirement_status(registration_id):
        """Get requirement submission status for a registration"""
        try:
            result = supabase.table("registration_requirements").select(
                "*, event_requirements!registration_requirements_requirement_id_fkey(*)"
            ).eq("registration_id", registration_id).execute()
            return result
        except Exception as e:
            print(f"Error fetching requirement status: {e}")
            return None

    @staticmethod
    def mark_requirement_submitted(registration_id, requirement_id):
        """Student marks a requirement as submitted"""
        try:
            # Check if already exists
            existing = supabase.table("registration_requirements").select("*").eq("registration_id", registration_id).eq("requirement_id", requirement_id).execute()
            
            if existing.data:
                # Update existing
                result = supabase.table("registration_requirements").update({
                    "student_submitted": True,
                    "submitted_at": "now()"
                }).eq("registration_id", registration_id).eq("requirement_id", requirement_id).execute()
            else:
                # Create new
                result = supabase.table("registration_requirements").insert({
                    "registration_id": registration_id,
                    "requirement_id": requirement_id,
                    "student_submitted": True,
                    "department_verified": False
                }).execute()
            
            return result
        except Exception as e:
            print(f"Error marking requirement submitted: {e}")
            return None

    @staticmethod
    def verify_requirement(registration_id, requirement_id, verified=True):
        """Department verifies a submitted requirement"""
        try:
            # Check if record exists
            existing = supabase.table("registration_requirements").select("*").eq(
                "registration_id", registration_id
            ).eq("requirement_id", requirement_id).execute()
            
            if existing.data:
                # Update existing record
                result = supabase.table("registration_requirements").update({
                    "department_verified": verified,
                    "verified_at": "now()" if verified else None
                }).eq("registration_id", registration_id).eq("requirement_id", requirement_id).execute()
            else:
                # Create new record (in case it wasn't initialized)
                result = supabase.table("registration_requirements").insert({
                    "registration_id": registration_id,
                    "requirement_id": requirement_id,
                    "student_submitted": False,
                    "department_verified": verified
                }).execute()
            
            return result
        except Exception as e:
            print(f"Error verifying requirement: {e}")
            return None

    @staticmethod
    def check_all_requirements_verified(registration_id):
        """Check if all requirements for a registration are verified"""
        try:
            # Get the event_id from registration
            registration = supabase.table("registrations").select("event_id").eq("id", registration_id).execute()
            if not registration.data:
                return False
            
            event_id = registration.data[0]["event_id"]
            
            # Get all requirements for the event
            event_reqs = supabase.table("event_requirements").select("id").eq("event_id", event_id).execute()
            if not event_reqs.data:
                return True  # No requirements means all verified
            
            total_requirements = len(event_reqs.data)
            
            # Get verified requirements for this registration
            verified_reqs = supabase.table("registration_requirements").select("id").eq("registration_id", registration_id).eq("department_verified", True).execute()
            
            verified_count = len(verified_reqs.data) if verified_reqs.data else 0
            
            return verified_count >= total_requirements
            
        except Exception as e:
            print(f"Error checking requirements: {e}")
            return False

    @staticmethod
    def initialize_requirements_for_registration(registration_id, event_id):
        """Initialize requirement tracking when a student registers"""
        try:
            # Get all requirements for the event
            requirements = EventRequirements.get_event_requirements(event_id)
            
            if not requirements or not requirements.data:
                return True  # No requirements to initialize
            
            # Get existing requirement records for this registration
            existing = supabase.table("registration_requirements").select("requirement_id").eq(
                "registration_id", registration_id
            ).execute()
            
            existing_req_ids = set()
            if existing.data:
                existing_req_ids = {item["requirement_id"] for item in existing.data}
            
            # Create entries for each requirement that doesn't exist yet
            for req in requirements.data:
                if req["id"] not in existing_req_ids:
                    supabase.table("registration_requirements").insert({
                        "registration_id": registration_id,
                        "requirement_id": req["id"],
                        "student_submitted": False,
                        "department_verified": False
                    }).execute()
            
            return True
        except Exception as e:
            print(f"Error initializing requirements: {e}")
            return False
