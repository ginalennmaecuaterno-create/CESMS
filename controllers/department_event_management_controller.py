from flask import render_template, request, redirect, url_for, flash, session
from models.event_management import EventManagement
from models.user import User

def view_department_events():
    """Display all events for a specific department management"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "department":
        flash("Access denied. Department accounts only.", "danger")
        return redirect(url_for("home"))
    
    try:
        # Get department ID from user
        department_id = user["id"]
        
        # Auto-update completed events in database
        EventManagement.auto_update_completed_events()
        
        # Get all events for this department
        events_response = EventManagement.get_events_by_department(department_id)
        events = events_response.data if events_response.data else []
        
        # Add display status to each event
        for event in events:
            event["display_status"] = EventManagement.get_event_display_status(event)
        
        # Get event counts for this department
        counts = EventManagement.get_event_counts_by_status_for_department(department_id)
        
        # Get filter from query parameters
        status_filter = request.args.get("status", "all")
        
        # Filter events if needed
        if status_filter != "all":
            events = [e for e in events if e["display_status"].lower() == status_filter.lower()]
        
        return render_template(
            "department_event_management.html",
            user=user,
            events=events,
            counts=counts,
            status_filter=status_filter
        )
        
    except Exception as e:
        flash(f"Error loading events: {str(e)}", "danger")
        return render_template(
            "department_event_management.html",
            user=user,
            events=[],
            counts={"Active": 0, "Completed": 0, "Cancelled": 0},
            status_filter="all"
        )


def cancel_department_event():
    """Cancel an event (only if it belongs to the department)"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "department":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("department_event_management.view_department_events"))
    
    try:
        department_id = user["id"]
        success, message = EventManagement.cancel_department_event(event_id, department_id)
        
        if success:
            flash(message, "success")
        else:
            flash(message, "danger")
            
    except Exception as e:
        flash(f"Error cancelling event: {str(e)}", "danger")
    
    return redirect(url_for("department_event_management.view_department_events"))


def postpone_department_event():
    """Postpone/reschedule an event (only if it belongs to the department)"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "department":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("department_event_management.view_department_events"))
    
    try:
        department_id = user["id"]
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("department_event_management.view_department_events"))
        
        event = event_response.data[0]
        
        # Verify event belongs to department
        if event["department_id"] != department_id:
            flash("You can only manage events from your own department.", "danger")
            return redirect(url_for("department_event_management.view_department_events"))
        
        if request.method == "POST":
            new_date = request.form.get("new_date")
            new_start_time = request.form.get("new_start_time")
            new_end_time = request.form.get("new_end_time")
            
            if not all([new_date, new_start_time, new_end_time]):
                flash("Please provide all required fields.", "danger")
                return render_template("department_postpone_event.html", user=user, event=event)
            
            success, message = EventManagement.postpone_department_event(
                event_id, department_id, new_date, new_start_time, new_end_time
            )
            
            if success:
                flash(message, "success")
                return redirect(url_for("department_event_management.view_department_events"))
            else:
                flash(message, "danger")
        
        return render_template("department_postpone_event.html", user=user, event=event)
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("department_event_management.view_department_events"))
