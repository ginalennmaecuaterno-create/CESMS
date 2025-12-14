from flask import render_template, redirect, url_for, flash, session
from models.user import User
from models.student_registrations import StudentRegistrations

def view_dashboard():
    """Display student dashboard with registration statistics"""
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
        # Get registration counts
        student_id = user["id"]
        counts = StudentRegistrations.get_registration_counts(student_id)
        
        return render_template(
            "student_dashboard.html",
            user=user,
            pending_count=counts.get("Pending", 0),
            approved_count=counts.get("Approved", 0),
            rejected_count=counts.get("Rejected", 0)
        )
        
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return render_template(
            "student_dashboard.html",
            user=user,
            pending_count=0,
            approved_count=0,
            rejected_count=0
        )
