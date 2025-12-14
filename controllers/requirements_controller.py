from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models.user import User
from models.event_requirements import EventRequirements
from models.event_registrations import EventRegistrations
from config import supabase

def manage_event_requirements():
    """Manage requirements for an event (Department)"""
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
    
    # Check if user is a department or OSAS
    if user["role"] not in ["department", "osas"]:
        flash("Access denied. Department or OSAS accounts only.", "danger")
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
        
        # Get requirements for this event
        requirements_response = EventRequirements.get_event_requirements(event_id)
        requirements = requirements_response.data if requirements_response and requirements_response.data else []
        
        return render_template(
            "department_manage_requirements.html",
            user=user,
            event=event,
            requirements=requirements
        )
        
    except Exception as e:
        flash(f"Error loading requirements: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))

def add_requirement():
    """Add a requirement to an event"""
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] not in ["department", "osas"]:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        data = request.get_json()
        event_id = data.get("event_id")
        requirement_name = data.get("requirement_name")
        description = data.get("description", "")
        
        if not event_id or not requirement_name:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        # Verify event belongs to department
        department_id = user_response.data[0]["id"]
        if not EventRegistrations.check_event_belongs_to_department(event_id, department_id):
            return jsonify({"success": False, "message": "Access denied"}), 403
        
        # Add requirement
        result = EventRequirements.add_requirement_to_event(event_id, requirement_name, description)
        
        if result and result.data:
            return jsonify({"success": True, "requirement": result.data[0]}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add requirement"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def delete_requirement():
    """Delete a requirement"""
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] not in ["department", "osas"]:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        requirement_id = request.args.get("requirement_id")
        
        if not requirement_id:
            return jsonify({"success": False, "message": "Requirement ID required"}), 400
        
        # Delete requirement
        result = EventRequirements.delete_requirement(requirement_id)
        
        if result:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Failed to delete"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def view_registration_requirements():
    """View and verify requirements for a specific registration (Department)"""
    if "user_email" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("user.login"))
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] not in ["department", "osas"]:
        flash("Access denied.", "danger")
        return redirect(url_for("user.login"))
    
    registration_id = request.args.get("registration_id")
    event_id = request.args.get("event_id")
    
    if not registration_id or not event_id:
        flash("Registration ID and Event ID required.", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))
    
    try:
        department_id = user["id"]
        
        # Verify event belongs to department
        if not EventRegistrations.check_event_belongs_to_department(event_id, department_id):
            flash("Access denied.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        # Get registration details
        registration = supabase.table("registrations").select(
            "*, users!registrations_student_id_fkey(full_name, student_id, email)"
        ).eq("id", registration_id).execute()
        
        if not registration.data:
            flash("Registration not found.", "danger")
            return redirect(url_for("event_registrations.view_event_registrations"))
        
        reg_data = registration.data[0]
        
        # Get event requirements
        event_reqs = EventRequirements.get_event_requirements(event_id)
        requirements = event_reqs.data if event_reqs and event_reqs.data else []
        
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
        
        return render_template(
            "department_verify_requirements.html",
            user=user,
            registration=reg_data,
            requirements=requirements_with_status,
            event_id=event_id
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("event_registrations.view_event_registrations"))

def toggle_requirement_verification():
    """Toggle requirement verification status"""
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] not in ["department", "osas"]:
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        data = request.get_json()
        registration_id = data.get("registration_id")
        requirement_id = data.get("requirement_id")
        verified = data.get("verified", False)
        
        if not registration_id or not requirement_id:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        # Verify requirement
        result = EventRequirements.verify_requirement(registration_id, requirement_id, verified)
        
        if result:
            # Check if all requirements are now verified
            all_verified = EventRequirements.check_all_requirements_verified(registration_id)
            
            return jsonify({
                "success": True,
                "all_verified": all_verified
            }), 200
        else:
            return jsonify({"success": False, "message": "Failed to update"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Student-side functions

def view_my_requirements():
    """View requirements for a student's registration"""
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
        event_id = event.get("id")
        
        # Get event requirements
        event_reqs = EventRequirements.get_event_requirements(event_id)
        requirements = event_reqs.data if event_reqs and event_reqs.data else []
        
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
        
        return render_template(
            "student_requirements.html",
            user=user,
            registration=reg_data,
            event=event,
            requirements=requirements_with_status
        )
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("student.view_registrations"))

def mark_requirement_submitted():
    """Student marks a requirement as submitted"""
    if "user_email" not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
    
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data or user_response.data[0]["role"] != "student":
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        data = request.get_json()
        registration_id = data.get("registration_id")
        requirement_id = data.get("requirement_id")
        
        if not registration_id or not requirement_id:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        student_id = user_response.data[0]["id"]
        
        # Verify registration belongs to this student
        registration = supabase.table("registrations").select("student_id").eq("id", registration_id).execute()
        if not registration.data or registration.data[0]["student_id"] != student_id:
            return jsonify({"success": False, "message": "Access denied"}), 403
        
        # Mark as submitted
        result = EventRequirements.mark_requirement_submitted(registration_id, requirement_id)
        
        if result:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
