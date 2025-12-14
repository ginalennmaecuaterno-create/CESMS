from flask import render_template, request, redirect, url_for, flash, session
from models.user import User
from config import supabase
from utils.email_service import EmailService
import re


def login():
    """Handle user login"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            # First, try Supabase Auth (for new users with email verification)
            try:
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if auth_response.user:
                    # Get user details from users table
                    user = User.get_user_by_email(email)
                    if user.data:
                        u = user.data[0]
                        
                        # Store user information in session
                        session["user_email"] = email
                        session["user_name"] = u.get("full_name", "User")
                        session["user_role"] = u.get("role", "student")
                        session["user_id"] = u.get("id")
                        session["student_id"] = u.get("student_id", "N/A")
                        session["department_name"] = u.get("department_name", "Department")
                        
                        flash("Login successful!", "success")

                        # Redirect based on role
                        if u["role"] == "osas":
                            return redirect(url_for("osas_dashboard"))
                        elif u["role"] == "department":
                            return redirect(url_for("department_dashboard"))
                        else:
                            return redirect(url_for("student.view_events"))
                    else:
                        flash("User not found in database.", "danger")
                        return render_template("login.html")
                        
            except Exception as auth_error:
                # If Supabase Auth fails, try direct database authentication (for old users)
                error_msg = str(auth_error)
                
                # Check if user exists in database
                user = User.get_user_by_email(email)
                if user.data:
                    u = user.data[0]
                    
                    # Verify password from database (for old users)
                    if u.get("password") == password:
                        # Store user information in session
                        session["user_email"] = email
                        session["user_name"] = u.get("full_name", "User")
                        session["user_role"] = u.get("role", "student")
                        session["user_id"] = u.get("id")
                        session["student_id"] = u.get("student_id", "N/A")
                        session["department_name"] = u.get("department_name", "Department")
                        
                        flash("Login successful!", "success")

                        # Redirect based on role
                        if u["role"] == "osas":
                            return redirect(url_for("osas_dashboard"))
                        elif u["role"] == "department":
                            return redirect(url_for("department_dashboard"))
                        else:
                            return redirect(url_for("student.view_events"))
                    else:
                        flash("Invalid email or password.", "danger")
                else:
                    # User doesn't exist in database
                    if "Invalid login credentials" in error_msg:
                        flash("Invalid email or password.", "danger")
                    elif "Email not confirmed" in error_msg:
                        flash("Please verify your email first.", "warning")
                    else:
                        flash("Invalid email or password.", "danger")

        except Exception as e:
            flash(f"Login failed: {str(e)}", "danger")

    return render_template("login.html")


def signup():
    """Handle user signup with email verification"""
    if request.method == "POST":
        full_name = request.form["full_name"]
        student_id = request.form["student_id"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            # Validate LSPU institutional email format
            email_pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@lspu\.edu\.ph$'
            if not re.match(email_pattern, email):
                flash("Please use your LSPU institutional email (firstname.lastname@lspu.edu.ph)", "danger")
                return redirect(url_for("user.signup"))
            
            # Check if email already exists in users table
            existing_email = User.get_user_by_email(email)
            if existing_email.data:
                flash("Email already registered. Please log in instead.", "danger")
                return redirect(url_for("user.signup"))

            # Check if student ID already exists
            existing_id = supabase.table("users").select("*").eq("student_id", student_id).execute()
            if existing_id.data:
                flash("Student ID already registered.", "danger")
                return redirect(url_for("user.signup"))

            # Validate password strength
            if len(password) < 8:
                flash("Password must be at least 8 characters long.", "danger")
                return redirect(url_for("user.signup"))
            if not re.search(r'[A-Z]', password):
                flash("Password must contain at least one uppercase letter.", "danger")
                return redirect(url_for("user.signup"))
            if not re.search(r'[a-z]', password):
                flash("Password must contain at least one lowercase letter.", "danger")
                return redirect(url_for("user.signup"))
            if not re.search(r'[0-9]', password):
                flash("Password must contain at least one number.", "danger")
                return redirect(url_for("user.signup"))

            # Store user data temporarily in session
            session["pending_signup"] = {
                "full_name": full_name,
                "student_id": student_id,
                "email": email,
                "password": password
            }

            # Send verification OTP
            success, message, otp = EmailService.send_verification_otp(email, full_name)
            
            if success:
                flash("Verification code sent to your email! Please check your inbox.", "success")
                return redirect(url_for("user.verify_email", email=email))
            else:
                # For development: show OTP in flash message if SendGrid not configured
                if otp:
                    flash(f"⚠️ SendGrid not configured. Your OTP is: {otp}", "warning")
                    return redirect(url_for("user.verify_email", email=email))
                else:
                    flash(f"Error sending verification email: {message}", "danger")
                    return redirect(url_for("user.signup"))

        except Exception as e:
            flash(f"Signup failed: {str(e)}", "danger")
            return redirect(url_for("user.signup"))

    return render_template("signup.html")


def verify_email():
    """Verify email with OTP"""
    email = request.args.get("email") or session.get("pending_signup", {}).get("email")
    
    if not email:
        flash("Invalid verification request.", "danger")
        return redirect(url_for("user.signup"))
    
    if request.method == "POST":
        otp = request.form["otp"]
        
        try:
            # Verify OTP
            success, message = EmailService.verify_otp(email, otp, "verification")
            
            if success:
                # Get pending signup data
                pending_data = session.get("pending_signup")
                
                if not pending_data:
                    flash("Session expired. Please sign up again.", "danger")
                    return redirect(url_for("user.signup"))
                
                # Register user in Supabase Auth
                auth_response = supabase.auth.sign_up({
                    "email": pending_data["email"],
                    "password": pending_data["password"],
                    "options": {
                        "email_redirect_to": None  # Disable default email verification
                    }
                })

                if auth_response.user:
                    # Manually confirm email in Supabase Auth
                    # Note: This requires admin privileges or service role key
                    # For now, we'll just create the user in our users table
                    
                    # Store in users table
                    User.create_user(
                        full_name=pending_data["full_name"],
                        student_id=pending_data["student_id"],
                        email=pending_data["email"],
                        password=pending_data["password"],
                        role="student"
                    )
                    
                    # Clear pending signup data
                    session.pop("pending_signup", None)
                    
                    flash("Email verified! Your account has been created successfully. Please log in.", "success")
                    return redirect(url_for("user.login"))
                else:
                    flash("Error creating account. Please try again.", "danger")
            else:
                flash(message, "danger")
                
        except Exception as e:
            flash(f"Verification failed: {str(e)}", "danger")
    
    return render_template("verify_email.html", email=email)


def resend_verification_otp():
    """Resend verification OTP"""
    email = request.form.get("email")
    
    if not email:
        flash("Invalid request.", "danger")
        return redirect(url_for("user.signup"))
    
    try:
        pending_data = session.get("pending_signup")
        if not pending_data:
            flash("Session expired. Please sign up again.", "danger")
            return redirect(url_for("user.signup"))
        
        full_name = pending_data.get("full_name", "User")
        
        # Send new OTP
        success, message, otp = EmailService.send_verification_otp(email, full_name)
        
        if success:
            flash("New verification code sent to your email!", "success")
        else:
            if otp:
                flash(f"⚠️ SendGrid not configured. Your OTP is: {otp}", "warning")
            else:
                flash(f"Error sending verification email: {message}", "danger")
                
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for("user.verify_email", email=email))


def forgot_password():
    """Request password reset"""
    if request.method == "POST":
        email = request.form["email"]
        
        try:
            # Validate email format
            email_pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@lspu\.edu\.ph$'
            if not re.match(email_pattern, email):
                flash("Please use your LSPU institutional email.", "danger")
                return redirect(url_for("user.forgot_password"))
            
            # Check if user exists
            user = User.get_user_by_email(email)
            if not user.data:
                # Don't reveal if email exists or not (security)
                flash("If this email is registered, you will receive a password reset code.", "success")
                return redirect(url_for("user.forgot_password"))
            
            user_data = user.data[0]
            full_name = user_data.get("full_name", "User")
            
            # Send password reset OTP
            success, message, otp = EmailService.send_password_reset_otp(email, full_name)
            
            if success:
                flash("Password reset code sent to your email!", "success")
                return redirect(url_for("user.verify_reset_otp", email=email))
            else:
                if otp:
                    flash(f"⚠️ SendGrid not configured. Your OTP is: {otp}", "warning")
                    return redirect(url_for("user.verify_reset_otp", email=email))
                else:
                    flash(f"Error sending reset code: {message}", "danger")
                    
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    
    return render_template("forgot_password.html")


def verify_reset_otp():
    """Verify password reset OTP"""
    email = request.args.get("email")
    
    if not email:
        flash("Invalid reset request.", "danger")
        return redirect(url_for("user.forgot_password"))
    
    if request.method == "POST":
        otp = request.form["otp"]
        
        try:
            # Verify OTP
            success, message = EmailService.verify_otp(email, otp, "reset")
            
            if success:
                # Store email in session for password reset
                session["reset_email"] = email
                flash("Code verified! Please set your new password.", "success")
                return redirect(url_for("user.reset_password"))
            else:
                flash(message, "danger")
                
        except Exception as e:
            flash(f"Verification failed: {str(e)}", "danger")
    
    return render_template("verify_reset_otp.html", email=email)


def resend_reset_otp():
    """Resend password reset OTP"""
    email = request.form.get("email")
    
    if not email:
        flash("Invalid request.", "danger")
        return redirect(url_for("user.forgot_password"))
    
    try:
        # Get user data
        user = User.get_user_by_email(email)
        if user.data:
            full_name = user.data[0].get("full_name", "User")
            
            # Send new OTP
            success, message, otp = EmailService.send_password_reset_otp(email, full_name)
            
            if success:
                flash("New reset code sent to your email!", "success")
            else:
                if otp:
                    flash(f"⚠️ SendGrid not configured. Your OTP is: {otp}", "warning")
                else:
                    flash(f"Error sending reset code: {message}", "danger")
        else:
            flash("If this email is registered, you will receive a password reset code.", "success")
                
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    
    return redirect(url_for("user.verify_reset_otp", email=email))


def reset_password():
    """Reset password after OTP verification"""
    email = session.get("reset_email")
    
    if not email:
        flash("Invalid reset request. Please start over.", "danger")
        return redirect(url_for("user.forgot_password"))
    
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        try:
            # Validate passwords match
            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return redirect(url_for("user.reset_password"))
            
            # Validate password strength
            if len(password) < 8:
                flash("Password must be at least 8 characters long.", "danger")
                return redirect(url_for("user.reset_password"))
            if not re.search(r'[A-Z]', password):
                flash("Password must contain at least one uppercase letter.", "danger")
                return redirect(url_for("user.reset_password"))
            if not re.search(r'[a-z]', password):
                flash("Password must contain at least one lowercase letter.", "danger")
                return redirect(url_for("user.reset_password"))
            if not re.search(r'[0-9]', password):
                flash("Password must contain at least one number.", "danger")
                return redirect(url_for("user.reset_password"))
            
            # Update password in Supabase Auth
            # Note: This requires the user to be signed in or use admin API
            # For now, we'll update the users table
            supabase.table("users").update({
                "password": password
            }).eq("email", email).execute()
            
            # Also update in Supabase Auth if possible
            try:
                # This would require admin privileges
                # For production, use Supabase Admin API
                pass
            except:
                pass
            
            # Clear reset session
            session.pop("reset_email", None)
            
            flash("Password reset successful! Please log in with your new password.", "success")
            return redirect(url_for("user.login"))
            
        except Exception as e:
            flash(f"Error resetting password: {str(e)}", "danger")
    
    return render_template("reset_password.html")


def logout():
    """Handle user logout"""
    try:
        # Sign out from Supabase
        supabase.auth.sign_out()
        
        # Clear session
        session.clear()
        
        flash("Logged out successfully.", "success")
    except Exception as e:
        flash(f"Logout error: {str(e)}", "danger")
    
    return redirect(url_for("user.login"))
