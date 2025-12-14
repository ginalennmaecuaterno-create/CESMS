from flask import render_template, request, redirect, url_for, flash, session
from models.user import User
from models.student_registrations import StudentRegistrations
import qrcode
from io import BytesIO
import base64

def view_registrations():
    """Display all student registrations with filtering"""
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
        
        # Get status filter from query parameters
        status_filter = request.args.get("status", "All")
        
        # Fetch registrations
        registrations_response = StudentRegistrations.get_student_registrations(
            student_id=student_id,
            status_filter=status_filter if status_filter != "All" else None
        )
        
        registrations = registrations_response.data if registrations_response and registrations_response.data else []
        
        # Enhance registrations with event status information and filter out completed events
        from models.event_management import EventManagement
        enhanced_registrations = []
        for reg in registrations:
            # Check if event is cancelled
            event = reg.get("events", {})
            event_status = event.get("status", "Active")
            reg["event_cancelled"] = event_status == "Cancelled"
            
            # Calculate display status
            display_status = EventManagement.get_event_display_status(event)
            
            # Filter out completed events - they should only appear in History
            if display_status != "Completed":
                enhanced_registrations.append(reg)
        
        # Sort by event date (ascending - soonest first)
        enhanced_registrations.sort(key=lambda x: x.get("events", {}).get("date", "9999-12-31"))
        
        return render_template(
            "student_registrations.html",
            user=user,
            registrations=enhanced_registrations,
            status_filter=status_filter
        )
        
    except Exception as e:
        flash(f"Error loading registrations: {str(e)}", "danger")
        return render_template(
            "student_registrations.html",
            user=user,
            registrations=[],
            status_filter="All"
        )

def cancel_registration(registration_id):
    """Cancel a pending registration"""
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
        
        # Attempt to cancel registration
        success = StudentRegistrations.cancel_registration(registration_id, student_id)
        
        if success:
            flash("Registration cancelled successfully.", "success")
        else:
            flash("Cannot cancel this registration. Only pending registrations can be cancelled.", "warning")
        
        return redirect(url_for("student.view_registrations"))
        
    except Exception as e:
        flash(f"Error cancelling registration: {str(e)}", "danger")
        return redirect(url_for("student.view_registrations"))

def view_ticket(registration_id):
    """Display QR code ticket for approved registration"""
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
        
        # Fetch registration with QR code
        registration_response = StudentRegistrations.get_registration_with_qr(registration_id, student_id)
        
        if not registration_response or not registration_response.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("student.view_registrations"))
        
        registration = registration_response.data[0]
        
        # Verify registration is approved
        if registration.get("registration_status") != "Approved":
            flash("Ticket is only available for approved registrations.", "warning")
            return redirect(url_for("student.view_registrations"))
        
        # Verify event is limited-seat (has participant_limit)
        event = registration.get("events", {})
        if event.get("participant_limit") is None:
            flash("Tickets are only available for limited-seat events.", "warning")
            return redirect(url_for("student.view_registrations"))
        
        # Get unique code
        unique_code = registration.get("unique_code")
        
        if not unique_code:
            flash("QR code not available for this registration.", "danger")
            return redirect(url_for("student.view_registrations"))
        
        # Generate QR code image
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(unique_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return render_template(
            "student_ticket.html",
            user=user,
            registration=registration,
            event=event,
            qr_code=qr_code_base64
        )
        
    except Exception as e:
        flash(f"Error loading ticket: {str(e)}", "danger")
        return redirect(url_for("student.view_registrations"))
