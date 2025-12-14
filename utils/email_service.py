import os
import random
import string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from config import supabase

class EmailService:
    """Service for sending emails via SendGrid"""
    
    @staticmethod
    def generate_otp(length=6):
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def send_email(to_email, subject, html_content):
        """Send email using SendGrid"""
        try:
            api_key = os.getenv('SENDGRID_API_KEY')
            from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@lspu.edu.ph')
            from_name = os.getenv('SENDGRID_FROM_NAME', 'LSPU CESMS')
            
            if not api_key or api_key == 'your_sendgrid_api_key_here':
                print("⚠️  SendGrid API key not configured. Email not sent.")
                print(f"📧 Would send to: {to_email}")
                print(f"📝 Subject: {subject}")
                return False, "SendGrid API key not configured"
            
            message = Mail(
                from_email=(from_email, from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False, str(e)
    
    @staticmethod
    def send_verification_otp(email, full_name):
        """Send OTP for email verification during signup"""
        try:
            # Generate OTP
            otp = EmailService.generate_otp()
            
            # Store OTP in database with expiration (10 minutes)
            expiration = datetime.now() + timedelta(minutes=10)
            
            # Delete any existing OTPs for this email
            supabase.table("email_verifications").delete().eq("email", email).execute()
            
            # Insert new OTP
            supabase.table("email_verifications").insert({
                "email": email,
                "otp": otp,
                "expires_at": expiration.isoformat(),
                "verified": False
            }).execute()
            
            # Email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1f2937 0%, #374151 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .otp-box {{ background: white; border: 2px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #1f2937; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px; }}
                    .button {{ display: inline-block; padding: 12px 24px; background: #1f2937; color: white; text-decoration: none; border-radius: 6px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎓 Welcome to LSPU CESMS</h1>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{full_name}</strong>,</p>
                        <p>Thank you for signing up for the Campus Event and Student Management System!</p>
                        <p>To verify your LSPU institutional email, please use the following One-Time Password (OTP):</p>
                        
                        <div class="otp-box">
                            <div class="otp-code">{otp}</div>
                            <p style="margin: 10px 0 0 0; color: #6b7280; font-size: 14px;">This code expires in 10 minutes</p>
                        </div>
                        
                        <p>If you didn't request this verification, please ignore this email.</p>
                        
                        <div class="footer">
                            <p>Laguna State Polytechnic University</p>
                            <p>Campus Event and Student Management System</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            success, message = EmailService.send_email(
                to_email=email,
                subject="Verify Your LSPU Email - OTP Code",
                html_content=html_content
            )
            
            return success, message, otp if not success else None
            
        except Exception as e:
            print(f"Error sending verification OTP: {e}")
            return False, str(e), None
    
    @staticmethod
    def send_password_reset_otp(email, full_name):
        """Send OTP for password reset"""
        try:
            # Generate OTP
            otp = EmailService.generate_otp()
            
            # Store OTP in database with expiration (10 minutes)
            expiration = datetime.now() + timedelta(minutes=10)
            
            # Delete any existing password reset OTPs for this email
            supabase.table("password_resets").delete().eq("email", email).execute()
            
            # Insert new OTP
            supabase.table("password_resets").insert({
                "email": email,
                "otp": otp,
                "expires_at": expiration.isoformat(),
                "used": False
            }).execute()
            
            # Email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .otp-box {{ background: white; border: 2px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #1f2937; }}
                    .warning {{ background: #f3f4f6; border-left: 4px solid #1f2937; padding: 12px; margin: 15px 0; border-radius: 4px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Password Reset Request</h1>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{full_name}</strong>,</p>
                        <p>We received a request to reset your password for your LSPU CESMS account.</p>
                        <p>Use the following One-Time Password (OTP) to reset your password:</p>
                        
                        <div class="otp-box">
                            <div class="otp-code">{otp}</div>
                            <p style="margin: 10px 0 0 0; color: #6b7280; font-size: 14px;">This code expires in 10 minutes</p>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Security Notice:</strong> If you didn't request a password reset, please ignore this email and ensure your account is secure.
                        </div>
                        
                        <div class="footer">
                            <p>Laguna State Polytechnic University</p>
                            <p>Campus Event and Student Management System</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            success, message = EmailService.send_email(
                to_email=email,
                subject="Password Reset Request - OTP Code",
                html_content=html_content
            )
            
            return success, message, otp if not success else None
            
        except Exception as e:
            print(f"Error sending password reset OTP: {e}")
            return False, str(e), None
    
    @staticmethod
    def verify_otp(email, otp, otp_type="verification"):
        """Verify OTP for email verification or password reset"""
        try:
            table = "email_verifications" if otp_type == "verification" else "password_resets"
            
            # Get OTP record
            response = supabase.table(table).select("*").eq("email", email).eq("otp", otp).execute()
            
            if not response.data:
                return False, "Invalid OTP code"
            
            record = response.data[0]
            
            # Check if already used (for password resets)
            if otp_type == "reset" and record.get("used"):
                return False, "OTP has already been used"
            
            # Check if already verified (for email verification)
            if otp_type == "verification" and record.get("verified"):
                return False, "Email already verified"
            
            # Check expiration
            expires_at = datetime.fromisoformat(record["expires_at"].replace('Z', '+00:00'))
            if datetime.now(expires_at.tzinfo) > expires_at:
                return False, "OTP has expired. Please request a new one"
            
            # Mark as verified/used
            if otp_type == "verification":
                supabase.table(table).update({"verified": True}).eq("id", record["id"]).execute()
            else:
                supabase.table(table).update({"used": True}).eq("id", record["id"]).execute()
            
            return True, "OTP verified successfully"
            
        except Exception as e:
            print(f"Error verifying OTP: {e}")
            return False, str(e)
