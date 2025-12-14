from flask import render_template, request, redirect, url_for, flash, session
from models.event_management import EventManagement
from models.user import User
from config import supabase

def view_all_events():
    """Display all events for OSAS management"""
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
    
    try:
        # Auto-update completed events in database
        EventManagement.auto_update_completed_events()
        
        # Get all events
        events_response = EventManagement.get_all_events()
        all_events = events_response.data if events_response.data else []
        
        # Add display_status to each event
        for event in all_events:
            event["display_status"] = EventManagement.get_event_display_status(event)
        
        # Calculate counts based on display_status (from ALL events)
        counts = {"Active": 0, "Ongoing": 0, "Completed": 0, "Cancelled": 0}
        for event in all_events:
            display_status = event["display_status"]
            counts[display_status] = counts.get(display_status, 0) + 1
        
        # Get filters from query parameters
        status_filter = request.args.get("status", "all")
        event_type_filter = request.args.get("event_type", "all")
        department_filter = request.args.get("department", "all")
        creator_filter = request.args.get("creator", "all")
        
        # Start with all events for filtering
        events = all_events.copy()
        
        # Filter by status (use display_status for filtering)
        if status_filter != "all":
            events = [e for e in events if e["display_status"].lower() == status_filter.lower()]
        
        # Filter by event type (limited vs free for all)
        if event_type_filter == "limited":
            events = [e for e in events if e.get("participant_limit") is not None]
        elif event_type_filter == "free":
            events = [e for e in events if e.get("participant_limit") is None]
        
        # Filter by creator (OSAS vs departments)
        if creator_filter == "osas":
            events = [e for e in events if e.get("users", {}).get("role") == "osas"]
        elif creator_filter == "departments":
            events = [e for e in events if e.get("users", {}).get("role") == "department"]
        
        # Filter by department
        if department_filter != "all":
            events = [e for e in events if e.get("users", {}).get("department_name") == department_filter]
        
        # Get unique departments for filter options
        all_departments = set()
        all_events_response = EventManagement.get_all_events()
        all_events = all_events_response.data if all_events_response.data else []
        for event in all_events:
            dept_name = event.get("users", {}).get("department_name")
            if dept_name:
                all_departments.add(dept_name)
        
        departments = sorted(list(all_departments))
        
        return render_template(
            "osas_event_management.html",
            user=user,
            events=events,
            counts=counts,
            status_filter=status_filter,
            event_type_filter=event_type_filter,
            department_filter=department_filter,
            creator_filter=creator_filter,
            departments=departments
        )
        
    except Exception as e:
        flash(f"Error loading events: {str(e)}", "danger")
        return render_template(
            "osas_event_management.html",
            user=user,
            events=[],
            counts={"Active": 0, "Completed": 0, "Cancelled": 0},
            status_filter="all",
            event_type_filter="all",
            department_filter="all",
            creator_filter="all",
            departments=[]
        )


def cancel_osas_event():
    """Cancel any event (OSAS has override authority)"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        success, message = EventManagement.cancel_event(event_id)
        
        if success:
            flash(message, "success")
        else:
            flash(message, "danger")
            
    except Exception as e:
        flash(f"Error cancelling event: {str(e)}", "danger")
    
    return redirect(url_for("osas_event_management.view_all_events"))


def postpone_osas_event():
    """Postpone/reschedule any event (OSAS has override authority)"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        if request.method == "POST":
            new_date = request.form.get("new_date")
            new_start_time = request.form.get("new_start_time")
            new_end_time = request.form.get("new_end_time")
            
            if not all([new_date, new_start_time, new_end_time]):
                flash("Please provide all required fields.", "danger")
                return render_template("osas_postpone_event.html", user=user, event=event)
            
            success, message = EventManagement.postpone_event(event_id, new_date, new_start_time, new_end_time)
            
            if success:
                flash(message, "success")
                return redirect(url_for("osas_event_management.view_all_events"))
            else:
                flash(message, "danger")
        
        return render_template("osas_postpone_event.html", user=user, event=event)
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))



def view_event_registrations():
    """OSAS views registrations for their own events only"""
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
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_registrations import EventRegistrations
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only view registrations for events you created.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Get all registrations for this event
        registrations_response = EventRegistrations.get_registrations_by_event(event_id)
        registrations = registrations_response.data if registrations_response.data else []
        
        # Get registration counts
        counts = EventRegistrations.get_registration_counts_by_event(event_id)
        
        return render_template(
            "osas_event_registrations.html",
            user=user,
            event=event,
            registrations=registrations,
            counts=counts
        )
        
    except Exception as e:
        flash(f"Error loading registrations: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))


def view_event_attendance():
    """OSAS views attendance for their own events only"""
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
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_registrations import EventRegistrations
        from config import supabase
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only view attendance for events you created.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Calculate display status
        display_status = EventManagement.get_event_display_status(event)
        event["display_status"] = display_status
        
        # Get attendance data
        attendance_response = supabase.table("registrations").select(
            "id, event_id, student_id, registration_status, attended, attended_at, users!registrations_student_id_fkey(full_name, email, student_id)"
        ).eq("event_id", event_id).eq("registration_status", "Approved").order("attended", desc=True).execute()
        
        attendance_list = attendance_response.data if attendance_response.data else []
        
        # Format attendance time for display (convert UTC to Philippine Time)
        for reg in attendance_list:
            if reg.get("attended_at"):
                from datetime import datetime, timedelta
                try:
                    # Parse UTC time
                    attended_dt = datetime.fromisoformat(reg["attended_at"].replace('Z', '+00:00'))
                    # Convert to Philippine Time (UTC+8)
                    ph_time = attended_dt + timedelta(hours=8)
                    reg["attendance_time"] = ph_time.strftime("%b %d, %Y %I:%M %p")
                except:
                    reg["attendance_time"] = reg["attended_at"]
            else:
                reg["attendance_time"] = None
        
        # Calculate statistics
        total_approved = len(attendance_list)
        total_attended = sum(1 for reg in attendance_list if reg.get("attended"))
        total_not_attended = total_approved - total_attended
        
        attendance_stats = {
            "total_approved": total_approved,
            "total_attended": total_attended,
            "total_not_attended": total_not_attended,
            "attendance_rate": round((total_attended / total_approved * 100) if total_approved > 0 else 0, 1)
        }
        
        return render_template(
            "osas_attendance.html",
            user=user,
            event=event,
            attendance_list=attendance_list,
            stats=attendance_stats
        )
        
    except Exception as e:
        flash(f"Error loading attendance: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))


def view_event_feedback():
    """OSAS views feedback for their own events only"""
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
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_feedback import EventFeedback
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only view feedback for events you created.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Get all feedback for this event
        feedback_response = EventFeedback.get_event_feedback(event_id)
        feedback_list = feedback_response.data if feedback_response and feedback_response.data else []
        
        # Get feedback summary
        summary = EventFeedback.get_event_feedback_summary(event_id)
        
        return render_template(
            "osas_event_feedback.html",
            user=user,
            event=event,
            feedback_list=feedback_list,
            summary=summary
        )
        
    except Exception as e:
        flash(f"Error loading feedback: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))



def view_registration_details():
    """OSAS views and manages registrations for their limited events"""
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
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_registrations import EventRegistrations
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only manage registrations for events you created.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Check if event is limited
        if event.get("participant_limit") is None:
            flash("This is a free-for-all event. No registration management needed.", "info")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Get all registrations
        registrations_response = EventRegistrations.get_registrations_by_event(event_id)
        all_registrations = registrations_response.data if registrations_response.data else []
        
        # Separate by status
        pending_registrations = [r for r in all_registrations if r["registration_status"] == "Pending"]
        approved_registrations = [r for r in all_registrations if r["registration_status"] == "Approved"]
        rejected_registrations = [r for r in all_registrations if r["registration_status"] == "Rejected"]
        
        # Get counts
        counts = EventRegistrations.get_registration_counts_by_event(event_id)
        
        return render_template(
            "osas_event_registration_details.html",
            user=user,
            event=event,
            pending_registrations=pending_registrations,
            approved_registrations=approved_registrations,
            rejected_registrations=rejected_registrations,
            counts=counts
        )
        
    except Exception as e:
        flash(f"Error loading registration details: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))


def approve_registration():
    """OSAS approves a registration"""
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    registration_id = request.args.get("registration_id")
    
    if not registration_id:
        flash("Registration ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_registrations import EventRegistrations
        
        # Get registration to find event_id
        reg_response = EventRegistrations.get_registration_by_id(registration_id)
        if not reg_response.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event_id = reg_response.data[0]["event_id"]
        
        # Approve registration
        EventRegistrations.approve_registration(registration_id)
        flash("Registration approved successfully!", "success")
        
        return redirect(url_for("osas_event_management.view_registration_details", event_id=event_id))
        
    except Exception as e:
        flash(f"Error approving registration: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))


def reject_registration():
    """OSAS rejects a registration"""
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    registration_id = request.args.get("registration_id")
    
    if not registration_id:
        flash("Registration ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_registrations import EventRegistrations
        
        # Get registration to find event_id
        reg_response = EventRegistrations.get_registration_by_id(registration_id)
        if not reg_response.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event_id = reg_response.data[0]["event_id"]
        
        # Reject registration
        EventRegistrations.reject_registration(registration_id)
        flash("Registration rejected.", "info")
        
        return redirect(url_for("osas_event_management.view_registration_details", event_id=event_id))
        
    except Exception as e:
        flash(f"Error rejecting registration: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))


def view_registration_requirements():
    """OSAS views requirements for a specific registration"""
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    user = user_response.data[0]
    registration_id = request.args.get("registration_id")
    
    if not registration_id:
        flash("Registration ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_requirements import EventRequirements
        
        # Get registration details
        registration = supabase.table("registrations").select(
            "*, users!registrations_student_id_fkey(full_name, student_id, email), events!registrations_event_id_fkey(id, event_name, department_id)"
        ).eq("id", registration_id).execute()
        
        if not registration.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        reg_data = registration.data[0]
        event = reg_data.get("events", {})
        event_id = event.get("id")
        
        # Check if event belongs to OSAS
        if event.get("department_id") != user["id"]:
            flash("Access denied.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Get event requirements
        event_reqs = EventRequirements.get_event_requirements(event_id)
        requirements = event_reqs.data if event_reqs and event_reqs.data else []
        
        # Initialize requirements for this registration if not already done
        if requirements:
            EventRequirements.initialize_requirements_for_registration(registration_id, event_id)
        
        # Get requirement status for this registration
        req_status = EventRequirements.get_student_requirement_status(registration_id)
        status_map = {}
        
        if req_status and req_status.data:
            for status in req_status.data:
                status_map[status["requirement_id"]] = status
        
        # Combine requirements with status
        requirements_with_status = []
        for req in requirements:
            req_with_status = req.copy()
            status = status_map.get(req["id"], {})
            req_with_status["student_submitted"] = status.get("student_submitted", False)
            req_with_status["department_verified"] = status.get("department_verified", False)
            req_with_status["submitted_at"] = status.get("submitted_at")
            req_with_status["verified_at"] = status.get("verified_at")
            requirements_with_status.append(req_with_status)
        
        # Use OSAS-specific template
        return render_template(
            "osas_verify_requirements.html",
            user=user,
            registration=reg_data,
            requirements=requirements_with_status,
            event_id=event_id
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))



def manage_event_requirements():
    """OSAS manages requirements for their events"""
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    user = user_response.data[0]
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        from models.event_requirements import EventRequirements
        
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only manage requirements for events you created.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Get requirements for this event
        requirements_response = EventRequirements.get_event_requirements(event_id)
        requirements = requirements_response.data if requirements_response and requirements_response.data else []
        
        return render_template(
            "osas_manage_requirements.html",
            user=user,
            event=event,
            requirements=requirements
        )
        
    except Exception as e:
        flash(f"Error loading requirements: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))



def scan_qr():
    """OSAS scans QR codes for attendance"""
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "osas":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))
    
    user = user_response.data[0]
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
    
    try:
        # Get event details
        event_response = EventManagement.get_event_by_id(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        event = event_response.data[0]
        
        # Check if event belongs to OSAS
        if event["department_id"] != user["id"]:
            flash("Access denied. You can only scan QR for events you created. This event belongs to another department/OSAS.", "danger")
            return redirect(url_for("osas_event_management.view_all_events"))
        
        # Calculate display status
        display_status = EventManagement.get_event_display_status(event)
        event["display_status"] = display_status
        
        # Use OSAS QR scanner template
        return render_template(
            "osas_qr_scanner.html",
            user=user,
            event=event
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("osas_event_management.view_all_events"))
