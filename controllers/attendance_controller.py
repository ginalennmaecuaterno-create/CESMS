from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models.user import User
from models.event_registrations import EventRegistrations
from config import supabase

def scan_qr():
    """Display QR code scanner page"""
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
    
    # Check if user is a department
    if user["role"] != "department":
        flash("Access denied. Department accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    try:
        department_id = user["id"]
        
        # Get all active events for this department
        events_response = supabase.table("events").select("*").eq("department_id", department_id).eq("status", "Active").order("date", desc=False).execute()
        all_events = events_response.data if events_response.data else []
        
        # Filter to show ONLY Ongoing events (not Active)
        from models.event_management import EventManagement
        scannable_events = []
        for event in all_events:
            display_status = EventManagement.get_event_display_status(event)
            # Only allow scanning for Ongoing events
            if display_status == "Ongoing":
                event["display_status"] = display_status
                scannable_events.append(event)
        
        return render_template(
            "department_qr_scanner.html",
            user=user,
            events=scannable_events
        )
        
    except Exception as e:
        flash(f"Error loading scanner: {str(e)}", "danger")
        return render_template(
            "department_qr_scanner.html",
            user=user,
            events=[]
        )

def verify_qr():
    """Verify QR code and mark attendance (API endpoint)"""
    # Check if user is logged in
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        return jsonify({"success": False, "message": "User not found"}), 401
    
    user = user_response.data[0]
    
    # Check if user is a department or OSAS
    if user["role"] not in ["department", "osas"]:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        data = request.get_json()
        unique_code = data.get("unique_code")
        event_id = data.get("event_id")
        
        if not unique_code or not event_id:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        organizer_id = user["id"]
        
        # Verify event belongs to this department/OSAS
        if not EventRegistrations.check_event_belongs_to_department(event_id, organizer_id):
            return jsonify({"success": False, "message": "Event does not belong to you"}), 403
        
        # Find registration by unique code and event
        registration_response = supabase.table("registrations").select(
            "*, users!registrations_student_id_fkey(full_name, student_id, email)"
        ).eq("unique_code", unique_code).eq("event_id", event_id).execute()
        
        if not registration_response.data:
            return jsonify({"success": False, "message": "Invalid QR code or event mismatch"}), 404
        
        registration = registration_response.data[0]
        
        # Check if registration is approved
        if registration.get("registration_status") != "Approved":
            return jsonify({"success": False, "message": "Registration not approved"}), 400
        
        # Check if already attended
        if registration.get("attended"):
            student_name = registration.get("users", {}).get("full_name", "Student")
            return jsonify({
                "success": False, 
                "message": f"{student_name} has already checked in",
                "already_attended": True,
                "student": registration.get("users")
            }), 400
        
        # Mark as attended
        supabase.table("registrations").update({
            "attended": True,
            "attended_at": "now()"
        }).eq("id", registration["id"]).execute()
        
        student = registration.get("users", {})
        
        return jsonify({
            "success": True,
            "message": "Attendance marked successfully!",
            "student": {
                "name": student.get("full_name", "Student"),
                "student_id": student.get("student_id", "N/A"),
                "email": student.get("email", "N/A")
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

def view_attendance():
    """View attendance report for an event"""
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
    
    # Check if user is a department
    if user["role"] != "department":
        flash("Access denied. Department accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    event_id = request.args.get("event_id")
    
    if not event_id:
        flash("Event ID is required.", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        department_id = user["id"]
        
        # Verify event belongs to this department
        if not EventRegistrations.check_event_belongs_to_department(event_id, department_id):
            flash("Access denied. This event does not belong to your department.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Get event details
        event_response = EventRegistrations.get_event_details(event_id)
        if not event_response.data:
            flash("Event not found.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        event = event_response.data[0]
        
        # Get display status for the event
        from models.event_management import EventManagement
        event_display_status = EventManagement.get_event_display_status(event)
        
        # Get all approved registrations with attendance status
        registrations_response = supabase.table("registrations").select(
            "id, event_id, student_id, registration_status, attended, attended_at, users!registrations_student_id_fkey(full_name, student_id, email)"
        ).eq("event_id", event_id).eq("registration_status", "Approved").order("attended", desc=True).execute()
        
        registrations = registrations_response.data if registrations_response.data else []
        
        # Format attendance time for display (convert UTC to Philippine Time)
        for reg in registrations:
            if reg.get("attended_at"):
                # Parse and format the timestamp
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
        total_approved = len(registrations)
        total_attended = sum(1 for r in registrations if r.get("attended"))
        attendance_rate = (total_attended / total_approved * 100) if total_approved > 0 else 0
        
        return render_template(
            "department_attendance.html",
            user=user,
            event=event,
            event_display_status=event_display_status,
            registrations=registrations,
            total_approved=total_approved,
            total_attended=total_attended,
            attendance_rate=round(attendance_rate, 1)
        )
        
    except Exception as e:
        flash(f"Error loading attendance: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
