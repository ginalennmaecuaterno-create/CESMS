from flask import Blueprint
from controllers import osas_event_management_controller

osas_event_management_bp = Blueprint("osas_event_management", __name__)

osas_event_management_bp.route("/osas/event-management", methods=["GET"])(osas_event_management_controller.view_all_events)
osas_event_management_bp.route("/osas/cancel-event", methods=["GET"])(osas_event_management_controller.cancel_osas_event)
osas_event_management_bp.route("/osas/postpone-event", methods=["GET", "POST"])(osas_event_management_controller.postpone_osas_event)
osas_event_management_bp.route("/osas/event-registrations", methods=["GET"])(osas_event_management_controller.view_event_registrations)
osas_event_management_bp.route("/osas/event-attendance", methods=["GET"])(osas_event_management_controller.view_event_attendance)
osas_event_management_bp.route("/osas/event-feedback", methods=["GET"])(osas_event_management_controller.view_event_feedback)
osas_event_management_bp.route("/osas/registration-details", methods=["GET"])(osas_event_management_controller.view_registration_details)
osas_event_management_bp.route("/osas/approve-registration", methods=["GET", "POST"])(osas_event_management_controller.approve_registration)
osas_event_management_bp.route("/osas/reject-registration", methods=["POST"])(osas_event_management_controller.reject_registration)
osas_event_management_bp.route("/osas/registration-requirements", methods=["GET"])(osas_event_management_controller.view_registration_requirements)
osas_event_management_bp.route("/osas/manage-requirements", methods=["GET"])(osas_event_management_controller.manage_event_requirements)
osas_event_management_bp.route("/osas/scan-qr", methods=["GET"])(osas_event_management_controller.scan_qr)