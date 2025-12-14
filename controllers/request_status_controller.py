from flask import render_template, request, redirect, url_for, flash, session
from models.request_status import RequestStatus
from models.user import User

def view_request_status():
    """Display all event requests with their status"""
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
    
    # Get filter from query parameters
    status_filter = request.args.get("status", "all")
    
    try:
        # Get requests based on filter
        if status_filter == "all":
            requests_response = RequestStatus.get_all_requests_by_department(user["id"])
        else:
            requests_response = RequestStatus.get_requests_by_status(user["id"], status_filter.capitalize())
        
        requests = requests_response.data if requests_response.data else []
        
        # Get status counts for summary
        status_counts = RequestStatus.count_requests_by_status(user["id"])
        
        return render_template(
            "department_request_status.html",
            user=user,
            requests=requests,
            status_filter=status_filter,
            status_counts=status_counts
        )
        
    except Exception as e:
        flash(f"Error loading requests: {str(e)}", "danger")
        return render_template(
            "department_request_status.html",
            user=user,
            requests=[],
            status_filter=status_filter,
            status_counts={"Pending": 0, "Approved": 0, "Rejected": 0, "Cancelled": 0}
        )


def delete_request():
    """Delete a pending event request"""
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
    
    request_id = request.args.get("id")
    
    if not request_id:
        flash("Request ID is required.", "danger")
        return redirect(url_for("request_status.view_request_status"))
    
    try:
        result = RequestStatus.delete_request_by_id(request_id, user["id"])
        
        if result:
            flash("Request deleted successfully.", "success")
        else:
            flash("Cannot delete this request. Only pending requests can be deleted.", "warning")
            
    except Exception as e:
        flash(f"Error deleting request: {str(e)}", "danger")
    
    return redirect(url_for("request_status.view_request_status"))


def edit_request():
    """Edit a pending event request"""
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
    
    request_id = request.args.get("id")
    
    if not request_id:
        flash("Request ID is required.", "danger")
        return redirect(url_for("request_status.view_request_status"))
    
    # Get the request details
    try:
        request_response = RequestStatus.get_request_details(request_id)
        
        if not request_response.data:
            flash("Request not found.", "danger")
            return redirect(url_for("request_status.view_request_status"))
        
        request_data = request_response.data[0]
        
        # Verify it belongs to this department and is pending
        if request_data["department_id"] != user["id"]:
            flash("Access denied. This request does not belong to you.", "danger")
            return redirect(url_for("request_status.view_request_status"))
        
        if request_data["status"] != "Pending":
            flash("Cannot edit this request. Only pending requests can be edited.", "warning")
            return redirect(url_for("request_status.view_request_status"))
        
        # Handle form submission
        if request.method == "POST":
            import json
            from config import supabase
            
            event_name = request.form.get("event_name")
            description = request.form.get("description")
            location = request.form.get("location")
            date = request.form.get("date")
            start_time = request.form.get("start_time")
            end_time = request.form.get("end_time")
            participant_limit = request.form.get("participant_limit")
            requirements_json = request.form.get("requirements")
            
            # Validation
            if not all([event_name, location, date, start_time, end_time]):
                flash("Please fill in all required fields.", "danger")
                return render_template("department_edit_request.html", user=user, request_data=request_data)
            
            try:
                # Convert participant_limit to int if provided
                if participant_limit and participant_limit.strip():
                    participant_limit = int(participant_limit)
                else:
                    participant_limit = None
                
                # Parse requirements if provided
                requirements = []
                if requirements_json:
                    try:
                        requirements = json.loads(requirements_json)
                    except:
                        requirements = []
                
                # Update the request
                result = RequestStatus.update_request(
                    request_id=request_id,
                    department_id=user["id"],
                    event_name=event_name,
                    description=description,
                    location=location,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    participant_limit=participant_limit
                )
                
                # Update requirements
                if result:
                    supabase.table("event_requests").update({
                        "requirements": requirements
                    }).eq("id", request_id).execute()
                    
                    flash("Request updated successfully!", "success")
                    return redirect(url_for("request_status.view_request_status"))
                else:
                    flash("Cannot update this request.", "warning")
                    
            except ValueError:
                flash("Participant limit must be a valid number.", "danger")
            except Exception as e:
                flash(f"Error updating request: {str(e)}", "danger")
        
        return render_template("department_edit_request.html", user=user, request_data=request_data)
        
    except Exception as e:
        flash(f"Error loading request: {str(e)}", "danger")
        return redirect(url_for("request_status.view_request_status"))


def cancel_request():
    """Cancel a pending event request by changing status to Cancelled"""
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
    
    request_id = request.args.get("id")
    
    if not request_id:
        flash("Request ID is required.", "danger")
        return redirect(url_for("request_status.view_request_status"))
    
    try:
        result = RequestStatus.cancel_request(request_id, user["id"])
        
        if result:
            flash("Request cancelled successfully. It will remain in your history.", "success")
        else:
            flash("Cannot cancel this request. Only pending requests can be cancelled.", "warning")
            
    except Exception as e:
        flash(f"Error cancelling request: {str(e)}", "danger")
    
    return redirect(url_for("request_status.view_request_status"))