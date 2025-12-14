from flask import Blueprint
from controllers import attendance_controller

attendance_bp = Blueprint("attendance", __name__, url_prefix="/department/attendance")

# QR Scanner routes
attendance_bp.route("/scan", methods=["GET"])(attendance_controller.scan_qr)
attendance_bp.route("/verify", methods=["POST"])(attendance_controller.verify_qr)

# Attendance report route
attendance_bp.route("/report", methods=["GET"])(attendance_controller.view_attendance)
