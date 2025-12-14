from flask import Blueprint
from controllers import requirements_controller

requirements_bp = Blueprint("requirements", __name__, url_prefix="/department/requirements")

# Department routes
requirements_bp.route("/manage", methods=["GET"])(requirements_controller.manage_event_requirements)
requirements_bp.route("/add", methods=["POST"])(requirements_controller.add_requirement)
requirements_bp.route("/delete", methods=["DELETE"])(requirements_controller.delete_requirement)
requirements_bp.route("/verify", methods=["GET"])(requirements_controller.view_registration_requirements)
requirements_bp.route("/toggle", methods=["POST"])(requirements_controller.toggle_requirement_verification)
