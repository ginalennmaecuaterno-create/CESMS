-- ============================================
-- CLEAN SYSTEM - Remove All Test Data
-- Keep Only User Accounts
-- ============================================

-- This script will delete all test data from the system
-- while preserving all user accounts (students, departments, OSAS)

BEGIN;

-- 1. Delete all feedback
DELETE FROM event_feedback;
DELETE FROM feedback;

-- 2. Delete all attendance records
DELETE FROM attendance;

-- 3. Delete all requirements
DELETE FROM registration_requirements;
DELETE FROM event_requirements;

-- 4. Delete all registrations
DELETE FROM registrations;

-- 5. Delete all events
DELETE FROM events;

-- 6. Delete all event requests
DELETE FROM event_requests;

-- 7. Delete email verification codes (optional - for fresh start)
DELETE FROM email_verifications;

-- 8. Delete password reset tokens (optional - for fresh start)  
DELETE FROM password_resets;

-- 9. Delete feedback
DELETE FROM feedback;

-- Reset auto-increment sequences (if any)
-- Note: PostgreSQL uses sequences, adjust if needed

-- Verify what's left (should only be users)
SELECT 'Users Count:' as info, COUNT(*) as count FROM users
UNION ALL
SELECT 'Events Count:', COUNT(*) FROM events
UNION ALL
SELECT 'Event Requests Count:', COUNT(*) FROM event_requests
UNION ALL
SELECT 'Registrations Count:', COUNT(*) FROM registrations
UNION ALL
SELECT 'Event Requirements Count:', COUNT(*) FROM event_requirements
UNION ALL
SELECT 'Registration Requirements Count:', COUNT(*) FROM registration_requirements
UNION ALL
SELECT 'Attendance Count:', COUNT(*) FROM attendance
UNION ALL
SELECT 'Event Feedback Count:', COUNT(*) FROM event_feedback
UNION ALL
SELECT 'Feedback Count:', COUNT(*) FROM feedback;

COMMIT;

-- ============================================
-- SUMMARY
-- ============================================
-- The following data has been DELETED:
-- ✓ All event feedback
-- ✓ All attendance records
-- ✓ All event requirements
-- ✓ All event registrations
-- ✓ All events (event_management)
-- ✓ All event requests
-- ✓ All email verification codes
-- ✓ All password reset tokens
--
-- The following data has been PRESERVED:
-- ✓ All user accounts (students, departments, OSAS)
--
-- System is now clean and ready for production use!
-- ============================================
