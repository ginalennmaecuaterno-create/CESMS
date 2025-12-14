from flask import render_template, request, redirect, url_for, flash, session
from models.event_registrations import EventRegistrations
from models.event_management import EventManagement
from models.user import User

def view_event_registrations():
    """Display all events with their registrations"""
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
    
    try:
        # Get all events for this department (including cancelled)
        events_response = EventRegistrations.get_all_department_events(user["id"])
        all_events = events_response.data if events_response.data else []
        
        # Add display_status and registration counts for each event
        events_with_counts = []
        for event in all_events:
            # Add display status
            event["display_status"] = EventManagement.get_event_display_status(event)
            
            # Get registration counts
            counts = EventRegistrations.get_registration_counts_by_event(event["id"])
            event["registration_counts"] = counts
            event["total_registrations"] = sum(counts.values())
            events_with_counts.append(event)
        
        # Calculate status counts for filter
        status_counts = {"Active": 0, "Ongoing": 0, "Completed": 0, "Cancelled": 0}
        for event in events_with_counts:
            display_status = event["display_status"]
            status_counts[display_status] = status_counts.get(display_status, 0) + 1
        
        # Get filter from query parameters
        status_filter = request.args.get("status", "all")
        
        # Filter events if needed
        if status_filter != "all":
            events_with_counts = [e for e in events_with_counts if e["display_status"].lower() == status_filter.lower()]
        
        return render_template(
            "department_event_registrations.html",
            user=user,
            events=events_with_counts,
            status_counts=status_counts,
            status_filter=status_filter
        )
        
    except Exception as e:
        flash(f"Error loading events: {str(e)}", "danger")
        return render_template(
            "department_event_registrations.html",
            user=user,
            events=[],
            status_counts={"Active": 0, "Ongoing": 0, "Completed": 0, "Cancelled": 0},
            status_filter="all"
        )


def view_event_registration_details():
    """Display registrations for a specific event"""
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
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        # Verify event belongs to this department
        if not EventRegistrations.check_event_belongs_to_department(event_id, user["id"]):
            flash("Access denied. This event does not belong to your department.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Get event details
        event_response = EventRegistrations.get_event_details(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        event = event_response.data[0]
        
        # Get registrations for this event
        registrations_response = EventRegistrations.get_registrations_by_event(event_id)
        registrations = registrations_response.data if registrations_response.data else []
        
        # Get registration counts
        counts = EventRegistrations.get_registration_counts_by_event(event_id)
        
        # Get filter from query parameters
        status_filter = request.args.get("status", "all")
        
        # Filter registrations if needed
        if status_filter != "all":
            registrations = [r for r in registrations if r["registration_status"].lower() == status_filter.lower()]
        
        return render_template(
            "department_event_registration_details.html",
            user=user,
            event=event,
            registrations=registrations,
            counts=counts,
            status_filter=status_filter
        )
        
    except Exception as e:
        flash(f"Error loading registrations: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))


def approve_registration():
    """Approve a registration and generate QR code"""
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
    
    registration_id = request.args.get("registration_id")
    event_id = request.args.get("event_id")
    
    if not registration_id or not event_id:
        flash("Registration ID and Event ID are required.", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        # Verify event belongs to this department
        if not EventRegistrations.check_event_belongs_to_department(event_id, user["id"]):
            flash("Access denied.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Approve registration
        result = EventRegistrations.approve_registration(registration_id)
        
        if result:
            flash("Registration approved successfully! QR code has been generated.", "success")
        else:
            flash("Error approving registration.", "danger")
            
    except Exception as e:
        flash(f"Error approving registration: {str(e)}", "danger")
    
    return redirect(url_for("event_registrations.view_event_registration_details", event_id=event_id))


def reject_registration():
    """Reject a registration"""
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
    
    registration_id = request.args.get("registration_id")
    event_id = request.args.get("event_id")
    
    if not registration_id or not event_id:
        flash("Registration ID and Event ID are required.", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        # Verify event belongs to this department
        if not EventRegistrations.check_event_belongs_to_department(event_id, user["id"]):
            flash("Access denied.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Reject registration
        result = EventRegistrations.reject_registration(registration_id)
        
        if result:
            flash("Registration rejected.", "success")
        else:
            flash("Error rejecting registration.", "danger")
            
    except Exception as e:
        flash(f"Error rejecting registration: {str(e)}", "danger")
    
    return redirect(url_for("event_registrations.view_event_registration_details", event_id=event_id))


def cancel_department_event():
    """Cancel an event (Department can only cancel their own events)"""
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
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        # Cancel the event (with department ownership check)
        success, message = EventRegistrations.cancel_event(event_id, user["id"])
        
        if success:
            flash(message, "success")
        else:
            flash(message, "danger")
            
    except Exception as e:
        flash(f"Error cancelling event: {str(e)}", "danger")
    
    return redirect(url_for("event_registrations.view_event_registrations"))


def postpone_department_event():
    """Show postpone event form"""
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
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        # Verify event belongs to this department
        if not EventRegistrations.check_event_belongs_to_department(event_id, user["id"]):
            flash("Access denied. This event does not belong to your department.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Get event details
        event_response = EventRegistrations.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        event = event_response.data[0]
        
        if request.method == "POST":
            new_date = request.form.get("new_date")
            new_start_time = request.form.get("new_start_time")
            new_end_time = request.form.get("new_end_time")
            
            if not all([new_date, new_start_time, new_end_time]):
                flash("Please provide all required fields.", "danger")
                return render_template("department_postpone_event.html", user=user, event=event)
            
            # Import EventManagement to use postpone function
            from models.event_management import EventManagement
            
            success, message = EventManagement.postpone_event(event_id, new_date, new_start_time, new_end_time)
            
            if success:
                flash(message, "success")
                return redirect(url_for("event_registrations.view_event_registrations"))
            else:
                flash(message, "danger")
        
        return render_template("department_postpone_event.html", user=user, event=event)
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))