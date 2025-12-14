from flask import Blueprint
from controllers import feedback_controller

feedback_bp = Blueprint("feedback", __name__)

# Student routes
feedback_bp.route("/student/feedback/submit", methods=["GET", "POST"])(feedback_controller.submit_feedback)

# Department routes
feedback_bp.route("/department/feedback/view", methods=["GET"])(feedback_controller.view_event_feedback)
