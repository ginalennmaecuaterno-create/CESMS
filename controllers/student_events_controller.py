from flask import render_template, redirect, url_for, flash, session
from models.user import User
from models.student_events import StudentEvents
from models.student_registrations import StudentRegistrations
from models.event_requirements import EventRequirements
from models.event_management import EventManagement
from models.event_feedback import EventFeedback
from config import supabase

def view_events():
    """Display all active events for students"""
    # Check if user is logged in
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    # Check if user is a student
    if user["role"] != "student":
        flash("Access denied. Student accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    try:
        student_id = user["id"]
        
        # Auto-update completed events in database
        from models.event_management import EventManagement
        EventManagement.auto_update_completed_events()
        
        # Fetch all active events
        events_response = StudentEvents.get_active_events()
        events = events_response.data if events_response and events_response.data else []
        
        # Enhance each event with additional information
        enhanced_events = []
        for event in events:
            # Calculate display status to filter out completed events
            display_status = EventManagement.get_event_display_status(event)
            
            # Only show Active and Ongoing events (exclude Completed)
            if display_status == "Completed":
                continue
            # Check if student has already registered
            has_registered = StudentRegistrations.has_registered(student_id, event["id"])
            
            # Determine event type
            is_free_for_all = event.get("participant_limit") is None
            is_limited = not is_free_for_all
            
            # Calculate available seats for limited events
            available_seats = 0
            is_full = False
            if is_limited:
                available_seats = StudentEvents.get_available_seats(event["id"])
                is_full = available_seats <= 0
            
            # Get requirements for this event (ONLY if limited, not free-for-all)
            requirements = []
            if is_limited and not is_free_for_all:
                req_response = EventRequirements.get_event_requirements(event["id"])
                requirements = req_response.data if req_response and req_response.data else []
            
            # Add enhanced data
            event["has_registered"] = has_registered
            event["is_free_for_all"] = is_free_for_all
            event["is_limited"] = is_limited
            event["available_seats"] = available_seats
            event["is_full"] = is_full
            event["requirements"] = requirements
            event["display_status"] = display_status  # Add display status for template
            
            enhanced_events.append(event)
        
        # Get unique organizers for filter dropdown
        organizers = set()
        for event in enhanced_events:
            if event.get("users"):
                if event["users"].get("role") == "osas":
                    organizers.add(("OSAS", "osas"))
                else:
                    dept_name = event["users"].get("department_name")
                    if dept_name:
                        organizers.add((dept_name, dept_name.lower().replace(" ", "_")))
        
        # Sort organizers: OSAS first, then departments alphabetically
        organizers_list = sorted(list(organizers), key=lambda x: (x[0] != "OSAS", x[0]))
        
        return render_template(
            "student_events.html",
            user=user,
            events=enhanced_events,
            organizers=organizers_list
        )
        
    except Exception as e:
        flash(f"Error loading events: {str(e)}", "danger")
        return render_template(
            "student_events.html",
            user=user,
            events=[]
        )

def register_for_event(event_id):
    """Handle event registration"""
    # Check if user is logged in
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    # Check if user is a student
    if user["role"] != "student":
        flash("Access denied. Student accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    try:
        student_id = user["id"]
        
        # Check if event exists and is active
        event_response = StudentEvents.get_event_by_id(event_id)
        if not event_response or not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("student.view_events"))
        
        event = event_response.data[0]
        
        # Check if event is active
        if event.get("status") != "Active":
            flash("This event is no longer accepting registrations.", "danger")
            return redirect(url_for("student.view_events"))
        
        # Check for duplicate registration
        if StudentRegistrations.has_registered(student_id, event_id):
            flash("You have already registered for this event.", "warning")
            return redirect(url_for("student.view_events"))
        
        # Determine event type
        is_free_for_all = event.get("participant_limit") is None
        
        # For limited-seat events, check if full
        if not is_free_for_all:
            if StudentEvents.is_event_full(event_id):
                flash("This event is full. No more seats available.", "danger")
                return redirect(url_for("student.view_events"))
        
        # Create registration
        # auto_approve=True for free-for-all, False for limited-seat
        result = StudentRegistrations.create_registration(
            student_id=student_id,
            event_id=event_id,
            auto_approve=is_free_for_all
        )
        
        if result and result.data:
            registration_id = result.data[0]["id"]
            
            # Initialize requirements for this registration (ONLY for limited events)
            if not is_free_for_all:
                EventRequirements.initialize_requirements_for_registration(registration_id, event_id)
            
            if is_free_for_all:
                flash("Registration successful! You're all set for this event.", "success")
            else:
                flash("Registration submitted! Awaiting department approval.", "success")
        else:
            flash("Error creating registration. Please try again.", "danger")
        
        return redirect(url_for("student.view_events"))
        
    except Exception as e:
        flash(f"Error registering for event: {str(e)}", "danger")
        return redirect(url_for("student.view_events"))


def view_event_history():
    """Display all completed events that the student attended"""
    # Check if user is logged in
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    # Check if user is a student
    if user["role"] != "student":
        flash("Access denied. Student accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    try:
        student_id = user["id"]
        
        # Auto-update completed events in database
        EventManagement.auto_update_completed_events()
        
        # Get all registrations for this student with completed events
        registrations_response = supabase.table("registrations").select(
            "*, events!registrations_event_id_fkey(*, users!events_department_id_fkey(department_name))"
        ).eq("student_id", student_id).execute()
        
        if not registrations_response.data:
            return render_template(
                "student_event_history.html",
                user=user,
                events=[]
            )
        
        # Filter for completed events and enhance with feedback info
        completed_events = []
        for reg in registrations_response.data:
            event = reg.get("events", {})
            if not event:
                continue
            
            # Calculate display status
            display_status = EventManagement.get_event_display_status(event)
            
            # Only include completed events
            if display_status != "Completed":
                continue
            
            # Check if student can give feedback
            # For limited events: must be attended (approved + marked as attended)
            # For free-for-all events: just needs to be registered (auto-approved)
            is_free_for_all = event.get("participant_limit") is None
            can_give_feedback = False
            
            if is_free_for_all:
                # Free-for-all: can give feedback if registered
                can_give_feedback = True
            else:
                # Limited: can give feedback only if attended
                can_give_feedback = reg.get("attended", False)
            
            # Check if feedback already submitted
            feedback_response = EventFeedback.get_feedback_by_registration(reg["id"])
            has_feedback = feedback_response and feedback_response.data
            existing_feedback = feedback_response.data[0] if has_feedback else None
            
            # Determine organizer name (OSAS or Department)
            event_user = event.get("users", {})
            if event_user.get("role") == "osas":
                organizer_name = "OSAS"
            else:
                organizer_name = event_user.get("department_name", "Unknown")
            
            # Add enhanced data
            event_data = {
                "registration_id": reg["id"],
                "event_id": event["id"],
                "event_name": event["event_name"],
                "description": event.get("description", ""),
                "location": event["location"],
                "date": event["date"],
                "start_time": event["start_time"],
                "end_time": event["end_time"],
                "department_name": organizer_name,
                "is_free_for_all": is_free_for_all,
                "attended": reg.get("attended", False),
                "can_give_feedback": can_give_feedback,
                "has_feedback": has_feedback,
                "existing_feedback": existing_feedback
            }
            
            completed_events.append(event_data)
        
        # Sort by date (most recent first)
        completed_events.sort(key=lambda x: x["date"], reverse=True)
        
        return render_template(
            "student_event_history.html",
            user=user,
            events=completed_events
        )
        
    except Exception as e:
        flash(f"Error loading event history: {str(e)}", "danger")
        return render_template(
            "student_event_history.html",
            user=user,
            events=[]
        )
