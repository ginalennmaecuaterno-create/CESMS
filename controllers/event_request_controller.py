from flask import render_template, request, redirect, url_for, flash, session
from models.event_request import EventRequest
from models.user import User
from config import supabase

def request_event():
    """Handle event request submission"""
    # Check if user is logged in and is a department
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "department":
        flash("Access denied. Department accounts only.", "danger")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        event_name = request.form.get("event_name")
        description = request.form.get("description")
        location = request.form.get("location")
        date = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        participant_limit = request.form.get("participant_limit")
        requirements_json = request.form.get("requirements")

        print(event_name, location, date, start_time, end_time, )
        
        # Validation
        if not all([event_name, location, date, start_time, end_time]):
            flash("Please fill in all required fields.", "danger")
            return render_template("department_request_event.html", user=user)
        
        # Check for schedule conflict before submission
        from models.event_request_management import EventRequestManagement
        has_conflict, conflicts = EventRequestManagement.check_schedule_conflict(
            location=location,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
        
        if has_conflict:
            # Build conflict message
            conflict_msg = "Schedule conflict detected! This time slot conflicts with: "
            conflict_details = []
            for c in conflicts:
                if c["type"] == "approved_event":
                    conflict_details.append(f"Approved Event '{c['name']}' ({c['time']})")
                else:
                    conflict_details.append(f"Pending Request '{c['name']}' ({c['time']})")
            conflict_msg += ", ".join(conflict_details)
            flash(conflict_msg, "danger")
            return render_template("department_request_event.html", user=user)
        
        try:
            import json
            
            # Convert participant_limit to int if provided
            if participant_limit and participant_limit.strip():
                participant_limit = int(participant_limit)
            else:
                participant_limit = None
            
            # Parse requirements if provided
            requirements = []
            if requirements_json:
                try:
                    requirements = json.loads(requirements_json)
                except:
                    requirements = []
            
            # Create event request with requirements as JSON
            response = EventRequest.create_event_request(
                department_id=user["id"],
                event_name=event_name,
                description=description,
                location=location,
                date=date,
                start_time=start_time,
                end_time=end_time,
                participant_limit=participant_limit
            )
            
            # Store requirements in the event_requests table as JSON
            if requirements and response.data:
                event_request_id = response.data[0]["id"]
                
                # Update the event request with requirements JSON
                supabase.table("event_requests").update({
                    "requirements": requirements
                }).eq("id", event_request_id).execute()
            
            flash("Event request submitted successfully! Awaiting OSAS approval.", "success")
            return redirect(url_for("event_request.request_event"))
            
        except ValueError:
            flash("Participant limit must be a valid number.", "danger")
        except Exception as e:
            flash(f"Error submitting request: {str(e)}", "danger")
    
    return render_template("department_request_event.html", user=user)