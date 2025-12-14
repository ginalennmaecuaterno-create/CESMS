# Authentication System Implementation Plan

## Overview
Implementing OTP-based email verification and password reset using SendGrid.

## New Features

### 1. Email Verification (Signup)
**Flow:**
1. User fills signup form
2. System sends OTP to institutional email
3. User enters OTP on verification page
4. Account activated after successful verification

**Pages:**
- `/signup` - Registration form
- `/verify-email` - OTP verification page
- `/resend-otp` - Resend OTP endpoint

### 2. Forgot Password
**Flow:**
1. User clicks "Forgot Password" on login page
2. User enters email
3. System sends OTP to email
4. User enters OTP
5. User sets new password

**Pages:**
- `/forgot-password` - Request password reset
- `/verify-reset-otp` - Verify OTP
- `/reset-password` - Set new password

## Database Tables

### email_verifications
- id (UUID)
- email (VARCHAR)
- otp (VARCHAR 6)
- expires_at (TIMESTAMP)
- verified (BOOLEAN)
- created_at (TIMESTAMP)

### password_resets
- id (UUID)
- email (VARCHAR)
- otp (VARCHAR 6)
- expires_at (TIMESTAMP)
- used (BOOLEAN)
- created_at (TIMESTAMP)

## SendGrid Configuration

Add to `.env`:
```
SENDGRID_API_KEY=your_api_key_here
SENDGRID_FROM_EMAIL=noreply@lspu.edu.ph
SENDGRID_FROM_NAME=LSPU CESMS
```

## Files to Create/Modify

### New Files:
- `utils/email_service.py` ✅
- `database_setup_email_verification.sql` ✅
- `templates/verify_email.html`
- `templates/forgot_password.html`
- `templates/verify_reset_otp.html`
- `templates/reset_password.html`

### Modified Files:
- `controllers/user_controller.py` - Add new endpoints
- `templates/login.html` - Add "Forgot Password" link
- `templates/signup.html` - Redirect to verification after signup
- `app.py` - Add new routes
- `requirements.txt` ✅

## Implementation Steps

1. ✅ Install SendGrid
2. ✅ Create email service utility
3. ✅ Create database migration
4. Create verification templates
5. Update user controller
6. Update login/signup templates
7. Add routes to app.py
8. Test flow

## Security Features

- OTP expires in 10 minutes
- OTP can only be used once
- Rate limiting on OTP requests
- Secure password requirements
- LSPU email validation

## Next Steps

Ready to implement the templates and controller updates?
