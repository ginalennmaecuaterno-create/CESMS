from flask import render_template, request, redirect, url_for, flash, session
from models.user import User
from models.event_management import EventManagement
from config import supabase

def create_osas_event():
    """OSAS creates their own event directly"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "osas":
        flash("Access denied. OSAS accounts only.", "danger")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        event_name = request.form.get("event_name")
        description = request.form.get("description")
        location = request.form.get("location")
        date = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        participant_limit = request.form.get("participant_limit")
        
        # Validation
        if not all([event_name, location, date, start_time, end_time]):
            flash("Please fill in all required fields.", "danger")
            return render_template("osas_create_event.html", user=user)
        
        try:
            # Convert participant_limit to int if provided
            if participant_limit and participant_limit.strip():
                participant_limit = int(participant_limit)
            else:
                participant_limit = None
            
            # Check for schedule conflict using the comprehensive check
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
                return render_template("osas_create_event.html", user=user)
            
            # Create event directly (OSAS is the organizer)
            osas_id = user["id"]
            
            result = supabase.table("events").insert({
                "department_id": osas_id,  # OSAS as organizer
                "event_name": event_name,
                "description": description,
                "location": location,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "participant_limit": participant_limit,
                "status": "Active"  # Directly active, no approval needed
            }).execute()
            
            if result.data:
                event_id = result.data[0]["id"]
                
                # Add requirements if this is a limited event
                if participant_limit:
                    import json
                    requirements_json = request.form.get("requirements", "[]")
                    try:
                        requirements = json.loads(requirements_json)
                        
                        from models.event_requirements import EventRequirements
                        for req in requirements:
                            EventRequirements.add_requirement_to_event(
                                event_id,
                                req.get("name"),
                                req.get("description", "")
                            )
                    except Exception as e:
                        print(f"Error adding requirements: {e}")
                
                flash("OSAS event created successfully!", "success")
                return redirect(url_for("osas_event_management.view_all_events"))
            else:
                flash("Error creating event.", "danger")
                
        except ValueError:
            flash("Participant limit must be a valid number.", "danger")
        except Exception as e:
            flash(f"Error creating event: {str(e)}", "danger")
    
    return render_template("osas_create_event.html", user=user)
