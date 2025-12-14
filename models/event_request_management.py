from config import supabase
from datetime import datetime, time

class EventRequestManagement:
    @staticmethod
    def get_all_pending_requests():
        """Get all pending event requests with department information"""
        requests = supabase.table("event_requests").select(
            "*, users!event_requests_department_id_fkey(full_name, department_name, email)"
        ).eq("status", "Pending").order("created_at", desc=True).execute()
        return requests

    @staticmethod
    def get_all_requests():
        """Get all event requests with department information"""
        requests = supabase.table("event_requests").select(
            "*, users!event_requests_department_id_fkey(full_name, department_name, email)"
        ).order("created_at", desc=True).execute()
        return requests
    
    @staticmethod
    def get_requests_by_status(status):
        """Get event requests by specific status"""
        requests = supabase.table("event_requests").select(
            "*, users!event_requests_department_id_fkey(full_name, department_name, email)"
        ).eq("status", status).order("created_at", desc=True).execute()
        return requests

    @staticmethod
    def get_request_by_id(request_id):
        """Get specific event request details"""
        return supabase.table("event_requests").select(
            "*, users!event_requests_department_id_fkey(full_name, department_name, email)"
        ).eq("id", request_id).execute()

    @staticmethod
    def check_schedule_conflict(location, date, start_time, end_time, exclude_request_id=None):
        """
        Check if there's a schedule conflict for the given location, date, and time
        Checks against:
        1. Active/Ongoing approved events
        2. Other pending requests
        Returns (has_conflict: bool, conflict_details: dict)
        """
        try:
            # Convert start_time and end_time to time objects for comparison
            if isinstance(start_time, str):
                # Try both formats: HH:MM:SS and HH:MM
                try:
                    new_start = datetime.strptime(start_time, "%H:%M:%S").time()
                except ValueError:
                    new_start = datetime.strptime(start_time, "%H:%M").time()
            else:
                new_start = start_time
                
            if isinstance(end_time, str):
                # Try both formats: HH:MM:SS and HH:MM
                try:
                    new_end = datetime.strptime(end_time, "%H:%M:%S").time()
                except ValueError:
                    new_end = datetime.strptime(end_time, "%H:%M").time()
            else:
                new_end = end_time
            
            conflicts = []
            
            # Check 1: Check against approved events (Active/Ongoing only, exclude Completed/Cancelled)
            approved_events = supabase.table("events").select("*").eq("location", location).eq("date", date).in_("status", ["Active"]).execute()
            
            if approved_events.data:
                for event in approved_events.data:
                    # Skip if this is the same request being updated
                    if exclude_request_id and event.get("event_request_id") == exclude_request_id:
                        continue
                    
                    # Convert existing event times
                    if isinstance(event["start_time"], str):
                        try:
                            existing_start = datetime.strptime(event["start_time"], "%H:%M:%S").time()
                        except ValueError:
                            existing_start = datetime.strptime(event["start_time"], "%H:%M").time()
                    else:
                        existing_start = event["start_time"]
                        
                    if isinstance(event["end_time"], str):
                        try:
                            existing_end = datetime.strptime(event["end_time"], "%H:%M:%S").time()
                        except ValueError:
                            existing_end = datetime.strptime(event["end_time"], "%H:%M").time()
                    else:
                        existing_end = event["end_time"]
                    
                    # Check for overlap: (StartA < EndB) and (EndA > StartB)
                    if (new_start < existing_end) and (new_end > existing_start):
                        conflicts.append({
                            "type": "approved_event",
                            "name": event["event_name"],
                            "time": f"{existing_start.strftime('%I:%M %p')} - {existing_end.strftime('%I:%M %p')}"
                        })
            
            # Check 2: Check against other pending requests
            pending_requests = supabase.table("event_requests").select("*").eq("location", location).eq("date", date).eq("status", "Pending").execute()
            
            if pending_requests.data:
                for req in pending_requests.data:
                    # Skip the current request
                    if exclude_request_id and req["id"] == exclude_request_id:
                        continue
                    
                    # Convert request times
                    if isinstance(req["start_time"], str):
                        try:
                            req_start = datetime.strptime(req["start_time"], "%H:%M:%S").time()
                        except ValueError:
                            req_start = datetime.strptime(req["start_time"], "%H:%M").time()
                    else:
                        req_start = req["start_time"]
                        
                    if isinstance(req["end_time"], str):
                        try:
                            req_end = datetime.strptime(req["end_time"], "%H:%M:%S").time()
                        except ValueError:
                            req_end = datetime.strptime(req["end_time"], "%H:%M").time()
                    else:
                        req_end = req["end_time"]
                    
                    # Check for overlap
                    if (new_start < req_end) and (new_end > req_start):
                        conflicts.append({
                            "type": "pending_request",
                            "name": req["event_name"],
                            "time": f"{req_start.strftime('%I:%M %p')} - {req_end.strftime('%I:%M %p')}"
                        })
            
            has_conflict = len(conflicts) > 0
            return has_conflict, conflicts
            
        except Exception as e:
            print(f"Error checking schedule conflict: {e}")
            return True, [{"type": "error", "name": "Error checking conflicts", "time": str(e)}]

    @staticmethod
    def approve_request(request_id):
        """
        Approve an event request and create the corresponding event
        Returns (success: bool, message: str)
        """
        try:
            # Get request details
            request_response = EventRequestManagement.get_request_by_id(request_id)
            
            if not request_response.data:
                return False, "Request not found"
            
            request_data = request_response.data[0]
            
            # Check if already processed
            if request_data["status"] != "Pending":
                return False, f"Request already {request_data['status'].lower()}"
            
            # Check for schedule conflict
            has_conflict, conflicts = EventRequestManagement.check_schedule_conflict(
                location=request_data["location"],
                date=request_data["date"],
                start_time=request_data["start_time"],
                end_time=request_data["end_time"],
                exclude_request_id=request_id
            )
            
            if has_conflict:
                # Build conflict message
                conflict_msg = "Schedule conflict detected with: "
                conflict_names = [c["name"] for c in conflicts]
                conflict_msg += ", ".join(conflict_names)
                
                return False, conflict_msg
            
            # No conflict - approve and create event
            # Update request status
            supabase.table("event_requests").update({
                "status": "Approved"
            }).eq("id", request_id).execute()
            
            # Create event
            event_response = supabase.table("events").insert({
                "event_request_id": request_id,
                "event_name": request_data["event_name"],
                "description": request_data["description"],
                "location": request_data["location"],
                "date": request_data["date"],
                "start_time": request_data["start_time"],
                "end_time": request_data["end_time"],
                "participant_limit": request_data["participant_limit"],
                "department_id": request_data["department_id"],
                "status": "Active"
            }).execute()
            
            # Copy requirements from event_requests to event_requirements
            if event_response.data and request_data.get("requirements"):
                event_id = event_response.data[0]["id"]
                requirements = request_data["requirements"]
                
                # If requirements is a list, add each one
                if isinstance(requirements, list):
                    for req_name in requirements:
                        supabase.table("event_requirements").insert({
                            "event_id": event_id,
                            "requirement_name": req_name,
                            "description": None
                        }).execute()
            
            return True, "Event request approved successfully!"
            
        except Exception as e:
            print(f"Error approving request: {e}")
            return False, f"Error approving request: {str(e)}"

    @staticmethod
    def reject_request(request_id):
        """
        Reject an event request
        Returns (success: bool, message: str)
        """
        try:
            # Get request details
            request_response = EventRequestManagement.get_request_by_id(request_id)
            
            if not request_response.data:
                return False, "Request not found"
            
            request_data = request_response.data[0]
            
            # Check if already processed
            if request_data["status"] != "Pending":
                return False, f"Request already {request_data['status'].lower()}"
            
            # Update request status to rejected
            supabase.table("event_requests").update({
                "status": "Rejected"
            }).eq("id", request_id).execute()
            
            return True, "Event request rejected."
            
        except Exception as e:
            print(f"Error rejecting request: {e}")
            return False, f"Error rejecting request: {str(e)}"

    @staticmethod
    def get_request_counts_by_status():
        """Get count of all requests grouped by status"""
        all_requests = supabase.table("event_requests").select("status").execute()
        
        counts = {"Pending": 0, "Approved": 0, "Rejected": 0, "Cancelled": 0}
        if all_requests.data:
            for req in all_requests.data:
                status = req.get("status", "Pending")
                counts[status] = counts.get(status, 0) + 1
        
        return counts
    
    @staticmethod
    def get_conflicts_for_requests(requests):
        """
        Check conflicts for a list of requests
        Returns a dictionary mapping request_id to conflict info
        """
        conflicts_map = {}
        
        for req in requests:
            if req["status"] == "Pending":
                has_conflict, conflicts = EventRequestManagement.check_schedule_conflict(
                    location=req["location"],
                    date=req["date"],
                    start_time=req["start_time"],
                    end_time=req["end_time"],
                    exclude_request_id=req["id"]
                )
                
                if has_conflict:
                    conflicts_map[req["id"]] = conflicts
        
        return conflicts_map