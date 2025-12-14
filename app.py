from flask import Flask, redirect, url_for, render_template, session, flash
from routes.user_routes import user_bp
from routes.event_request_routes import event_request_bp
from routes.request_status_routes import request_status_bp
from routes.event_registrations_routes import event_registrations_bp
from routes.event_request_management_routes import event_request_management_bp
from routes.osas_event_management_routes import osas_event_management_bp
from routes.osas_create_event_routes import osas_create_event_bp
from routes.department_event_management_routes import department_event_management_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.requirements_routes import requirements_bp
from routes.feedback_routes import feedback_bp
from utils.time_formatter import format_time_12hr, format_date_readable, format_datetime_readable
import os

app = Flask(__name__)

# Use environment variable for secret key in production
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_fallback_for_local_dev')

# Register custom Jinja2 filters for time formatting
app.jinja_env.filters['time_12hr'] = format_time_12hr
app.jinja_env.filters['date_readable'] = format_date_readable
app.jinja_env.filters['datetime_readable'] = format_datetime_readable

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(event_request_bp)
app.register_blueprint(request_status_bp)
app.register_blueprint(event_registrations_bp)
app.register_blueprint(event_request_management_bp)
app.register_blueprint(osas_event_management_bp)
app.register_blueprint(osas_create_event_bp)
app.register_blueprint(department_event_management_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(requirements_bp)
app.register_blueprint(feedback_bp)


@app.route("/")
def home():
    return redirect(url_for("user.login"))

@app.route("/department/dashboard")
def department_dashboard():
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    from models.user import User
    from models.event_management import EventManagement
    from models.event_request_management import EventRequestManagement
    from config import supabase
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "department":
        flash("Access denied. Department accounts only.", "danger")
        return redirect(url_for("home"))
    
    department_id = user["id"]
    
    try:
        # Get department's events by status
        events_response = supabase.table("events").select("*").eq("department_id", department_id).execute()
        all_events = events_response.data if events_response.data else []
        
        event_counts = {
            "Active": len([e for e in all_events if e.get("status") == "Active"]),
            "Ongoing": len([e for e in all_events if e.get("status") == "Ongoing"]),
            "Completed": len([e for e in all_events if e.get("status") == "Completed"]),
            "Cancelled": len([e for e in all_events if e.get("status") == "Cancelled"])
        }
        
        # Get department's event requests
        requests_response = supabase.table("event_requests").select("*").eq("department_id", department_id).execute()
        all_requests = requests_response.data if requests_response.data else []
        
        request_counts = {
            "Pending": len([r for r in all_requests if r.get("status") == "Pending"]),
            "Approved": len([r for r in all_requests if r.get("status") == "Approved"]),
            "Rejected": len([r for r in all_requests if r.get("status") == "Rejected"])
        }
        
        # Get registrations for department's events
        event_ids = [e["id"] for e in all_events]
        if event_ids:
            registrations_response = supabase.table("registrations").select("*").in_("event_id", event_ids).execute()
            all_registrations = registrations_response.data if registrations_response.data else []
        else:
            all_registrations = []
        
        total_registrations = len(all_registrations)
        pending_registrations = len([r for r in all_registrations if r.get("registration_status") == "Pending"])
        
        stats = {
            "total_events": len(all_events),
            "active_events": event_counts.get("Active", 0),
            "completed_events": event_counts.get("Completed", 0),
            "pending_requests": request_counts.get("Pending", 0),
            "total_registrations": total_registrations,
            "pending_registrations": pending_registrations
        }
        
        # Calculate KPI Metrics
        # 1. Event Success Rate
        total_events_for_success = event_counts.get("Active", 0) + event_counts.get("Completed", 0) + event_counts.get("Cancelled", 0)
        completed_events = event_counts.get("Completed", 0)
        event_success_rate = round((completed_events / total_events_for_success * 100) if total_events_for_success > 0 else 0, 1)
        
        # 2. Attendance Rate
        approved_registrations = [r for r in all_registrations if r.get("registration_status") == "Approved"]
        total_approved = len(approved_registrations)
        total_attended = len([r for r in approved_registrations if r.get("attended")])
        attendance_rate = round((total_attended / total_approved * 100) if total_approved > 0 else 0, 1)
        
        # 3. Unique Participants
        unique_participants = len(set([r["student_id"] for r in all_registrations if r.get("attended")])) if all_registrations else 0
        
        # 4. Event Feedback Score
        if event_ids:
            feedback_response = supabase.table("event_feedback").select("rating").in_("event_id", event_ids).execute()
            all_feedback = feedback_response.data if feedback_response.data else []
        else:
            all_feedback = []
        
        total_feedback = len(all_feedback)
        avg_rating = round(sum([f["rating"] for f in all_feedback]) / total_feedback, 1) if total_feedback > 0 else 0
        
        # 5. Registration Approval Rate
        approved_count = len([r for r in all_registrations if r.get("registration_status") == "Approved"])
        registration_approval_rate = round((approved_count / total_registrations * 100) if total_registrations > 0 else 0, 1)
        
        kpi = {
            "event_success_rate": event_success_rate,
            "completed_events": completed_events,
            "total_events_for_success": total_events_for_success,
            "attendance_rate": attendance_rate,
            "total_attended": total_attended,
            "total_approved": total_approved,
            "unique_participants": unique_participants,
            "feedback_score": avg_rating,
            "total_feedback": total_feedback,
            "registration_approval_rate": registration_approval_rate,
            "approved_registrations": approved_count,
            "total_registrations": total_registrations
        }
        
        # Get recent events (last 5)
        recent_events = sorted(all_events, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
        
        # Get pending requests (last 5)
        pending_requests = [r for r in all_requests if r.get("status") == "Pending"][:5]
        
        return render_template(
            "department_dashboard.html",
            user=user,
            stats=stats,
            kpi=kpi,
            recent_events=recent_events,
            pending_requests=pending_requests
        )
        
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return render_template("department_dashboard.html", user=user, stats={}, kpi={}, recent_events=[], pending_requests=[])

@app.route("/osas/dashboard")
def osas_dashboard():
    if "user_email" not in session:
        return redirect(url_for("user.login"))
    
    from models.user import User
    from models.event_management import EventManagement
    from models.event_request_management import EventRequestManagement
    from config import supabase
    
    # Get user details
    user_response = User.get_user_by_email(session["user_email"])
    if not user_response.data:
        flash("User not found.", "danger")
        return redirect(url_for("user.login"))
    
    user = user_response.data[0]
    
    if user["role"] != "osas":
        flash("Access denied. OSAS accounts only.", "danger")
        return redirect(url_for("home"))
    
    try:
        # Get statistics
        event_counts = EventManagement.get_event_counts_by_status()
        request_counts = EventRequestManagement.get_request_counts_by_status()
        
        # Get total registrations
        all_registrations = supabase.table("registrations").select("id, registration_status").execute()
        total_registrations = len(all_registrations.data) if all_registrations.data else 0
        pending_registrations = len([r for r in all_registrations.data if r.get("registration_status") == "Pending"]) if all_registrations.data else 0
        
        stats = {
            "total_events": sum(event_counts.values()),
            "active_events": event_counts.get("Active", 0),
            "completed_events": event_counts.get("Completed", 0),
            "pending_requests": request_counts.get("Pending", 0),
            "total_registrations": total_registrations,
            "pending_registrations": pending_registrations
        }
        
        # Calculate KPI Metrics
        # 1. Event Success Rate
        total_events_for_success = event_counts.get("Active", 0) + event_counts.get("Completed", 0)
        completed_events = event_counts.get("Completed", 0)
        event_success_rate = round((completed_events / total_events_for_success * 100) if total_events_for_success > 0 else 0, 1)
        
        # 2. Attendance Rate
        all_attendance = supabase.table("registrations").select("attended, registration_status").eq("registration_status", "Approved").execute()
        total_approved = len(all_attendance.data) if all_attendance.data else 0
        total_attended = len([a for a in all_attendance.data if a.get("attended")]) if all_attendance.data else 0
        attendance_rate = round((total_attended / total_approved * 100) if total_approved > 0 else 0, 1)
        
        # 3. Request Approval Time (simplified - using created_at from requests)
        processed_requests = request_counts.get("Approved", 0) + request_counts.get("Rejected", 0)
        avg_approval_time = "< 24h"  # Simplified for now
        
        # 4. Student Participation (unique students who attended)
        unique_participants_query = supabase.table("registrations").select("student_id").eq("attended", True).execute()
        unique_participants = len(set([r["student_id"] for r in unique_participants_query.data])) if unique_participants_query.data else 0
        
        # 5. Event Feedback Score
        all_feedback = supabase.table("event_feedback").select("rating").execute()
        total_feedback = len(all_feedback.data) if all_feedback.data else 0
        avg_rating = round(sum([f["rating"] for f in all_feedback.data]) / total_feedback, 1) if total_feedback > 0 else 0
        
        # 6. Registration Completion Rate
        approved_registrations = len([r for r in all_registrations.data if r.get("registration_status") == "Approved"]) if all_registrations.data else 0
        registration_completion_rate = round((approved_registrations / total_registrations * 100) if total_registrations > 0 else 0, 1)
        
        kpi = {
            "event_success_rate": event_success_rate,
            "completed_events": completed_events,
            "total_events_for_success": total_events_for_success,
            "attendance_rate": attendance_rate,
            "total_attended": total_attended,
            "total_approved": total_approved,
            "avg_approval_time": avg_approval_time,
            "processed_requests": processed_requests,
            "unique_participants": unique_participants,
            "feedback_score": avg_rating,
            "total_feedback": total_feedback,
            "registration_completion_rate": registration_completion_rate,
            "approved_registrations": approved_registrations,
            "total_registrations": total_registrations
        }
        
        # Get recent events
        recent_events_response = EventManagement.get_all_events()
        recent_events = recent_events_response.data[:10] if recent_events_response.data else []
        
        # Get pending requests
        pending_requests_response = EventRequestManagement.get_all_pending_requests()
        pending_requests = pending_requests_response.data[:10] if pending_requests_response.data else []
        
        return render_template(
            "osas_dashboard.html",
            user=user,
            stats=stats,
            kpi=kpi,
            recent_events=recent_events,
            pending_requests=pending_requests
        )
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        default_kpi = {
            "event_success_rate": 0, "completed_events": 0, "total_events_for_success": 0,
            "attendance_rate": 0, "total_attended": 0, "total_approved": 0,
            "avg_approval_time": "N/A", "processed_requests": 0,
            "unique_participants": 0, "feedback_score": 0, "total_feedback": 0,
            "registration_completion_rate": 0, "approved_registrations": 0, "total_registrations": 0
        }
        return render_template("osas_dashboard.html", user=user, stats={}, kpi=default_kpi, recent_events=[], pending_requests=[])

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.getenv('PORT', 5000))
    # Debug mode off in production
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)