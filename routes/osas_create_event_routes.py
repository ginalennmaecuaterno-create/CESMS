from flask import Blueprint
from controllers import osas_create_event_controller

osas_create_event_bp = Blueprint("osas_create_event", __name__, url_prefix="/osas")

# OSAS Create Event routes
osas_create_event_bp.route("/create-event", methods=["GET", "POST"])(osas_create_event_controller.create_osas_event)
