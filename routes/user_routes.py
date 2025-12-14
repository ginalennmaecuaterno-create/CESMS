from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint("user", __name__)

# Authentication routes
user_bp.route("/login", methods=["GET", "POST"])(user_controller.login)
user_bp.route("/signup", methods=["GET", "POST"])(user_controller.signup)
user_bp.route("/logout", methods=["GET"])(user_controller.logout)

# Email verification routes
user_bp.route("/verify-email", methods=["GET", "POST"])(user_controller.verify_email)
user_bp.route("/resend-verification-otp", methods=["POST"])(user_controller.resend_verification_otp)

# Password reset routes
user_bp.route("/forgot-password", methods=["GET", "POST"])(user_controller.forgot_password)
user_bp.route("/verify-reset-otp", methods=["GET", "POST"])(user_controller.verify_reset_otp)
user_bp.route("/resend-reset-otp", methods=["POST"])(user_controller.resend_reset_otp)
user_bp.route("/reset-password", methods=["GET", "POST"])(user_controller.reset_password)