from flask import Blueprint, redirect, url_for
from controllers import student_dashboard_controller, student_events_controller, student_registrations_controller, requirements_controller

student_bp = Blueprint("student", __name__, url_prefix="/student")

# Dashboard routes - Redirect to events
@student_bp.route("/dashboard", methods=["GET"])
def redirect_to_events():
    return redirect(url_for('student.view_events'))

# Events routes
student_bp.route("/events", methods=["GET"])(student_events_controller.view_events)
student_bp.route("/events/register/<event_id>", methods=["POST"])(student_events_controller.register_for_event)
student_bp.route("/event-history", methods=["GET"])(student_events_controller.view_event_history)

# Registrations routes
student_bp.route("/registrations", methods=["GET"])(student_registrations_controller.view_registrations)
student_bp.route("/registrations/cancel/<registration_id>", methods=["POST"])(student_registrations_controller.cancel_registration)
student_bp.route("/ticket/<registration_id>", methods=["GET"])(student_registrations_controller.view_ticket)

# Requirements routes
student_bp.route("/requirements/view", methods=["GET"])(requirements_controller.view_my_requirements)
student_bp.route("/requirements/submit", methods=["POST"])(requirements_controller.mark_requirement_submitted)
