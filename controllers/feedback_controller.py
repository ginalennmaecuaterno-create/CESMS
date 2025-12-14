from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models.user import User
from models.event_feedback import EventFeedback
from models.event_registrations import EventRegistrations
from config import supabase

# Student-side functions

def submit_feedback():
    """Student submits feedback for an event they attended"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "student":
        flash("Access denied. Student accounts only.", "danger")
        return redirect(url_for("user.login"))
    
    registration_id = request.args.get("registration_id")
    
    if not registration_id:
        flash("Registration ID is required.", "danger")
        return redirect(url_for("student.view_registrations"))
    
    try:
        student_id = user["id"]
        
        # Get registration details and verify it belongs to this student
        registration = supabase.table("registrations").select(
            "*, events!registrations_event_id_fkey(*)"
        ).eq("id", registration_id).eq("student_id", student_id).execute()
        
        if not registration.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("student.view_registrations"))
        
        reg_data = registration.data[0]
        event = reg_data.get("events", {})
        
        # Check if event is completed
        from models.event_management import EventManagement
        display_status = EventManagement.get_event_display_status(event)
        
        if display_status != "Completed":
            flash("You can only submit feedback for completed events.", "warning")
            return redirect(url_for("student.view_event_history"))
        
        # Check if student can give feedback
        # For limited events: must be attended (approved + marked as attended)
        # For free-for-all events: just needs to be registered (auto-approved)
        is_free_for_all = event.get("participant_limit") is None
        
        if not is_free_for_all and not reg_data.get("attended"):
            flash("You can only submit feedback for events you attended.", "warning")
            return redirect(url_for("student.view_event_history"))
        
        # Check if feedback already submitted
        existing_feedback = EventFeedback.get_feedback_by_registration(registration_id)
        has_feedback = existing_feedback and existing_feedback.data
        
        if request.method == "POST":
            rating = request.form.get("rating")
            comment = request.form.get("comment", "").strip()
            
            if not rating:
                flash("Please provide a rating.", "danger")
                return render_template(
                    "student_submit_feedback.html",
                    user=user,
                    registration=reg_data,
                    event=event,
                    existing_feedback=existing_feedback.data[0] if has_feedback else None
                )
            
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5")
                
                if has_feedback:
                    # Update existing feedback
                    result = EventFeedback.update_feedback(registration_id, rating, comment)
                    message = "Feedback updated successfully!"
                else:
                    # Submit new feedback
                    result = EventFeedback.submit_feedback(
                        registration_id, event["id"], student_id, rating, comment
                    )
                    message = "Thank you for your feedback!"
                
                if result:
                    flash(message, "success")
                    return redirect(url_for("student.view_event_history"))
                else:
                    flash("Error submitting feedback. Please try again.", "danger")
                    
            except ValueError as e:
                flash(str(e), "danger")
        
        return render_template(
            "student_submit_feedback.html",
            user=user,
            registration=reg_data,
            event=event,
            existing_feedback=existing_feedback.data[0] if has_feedback else None
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("student.view_event_history"))


# Department-side functions

def view_event_feedback():
    """Department views feedback for their event"""
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
        
        # Get all feedback for this event
        feedback_response = EventFeedback.get_event_feedback(event_id)
        feedback_list = feedback_response.data if feedback_response and feedback_response.data else []
        
        # Get feedback summary
        summary = EventFeedback.get_event_feedback_summary(event_id)
        
        return render_template(
            "department_event_feedback.html",
            user=user,
            event=event,
            feedback_list=feedback_list,
            summary=summary
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
