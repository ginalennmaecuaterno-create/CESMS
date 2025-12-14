-- ============================================
-- ADD ONGOING OSAS EVENT FOR ATTENDANCE TESTING
-- Event happening TODAY with correct timezone
-- ============================================

BEGIN;

-- Add OSAS ongoing event (Limited, happening TODAY)
INSERT INTO events (
    id, 
    event_name, 
    description, 
    location, 
    date, 
    start_time, 
    end_time, 
    participant_limit, 
    department_id, 
    status, 
    created_at
) VALUES (
    gen_random_uuid(),
    'LSPU Student Leadership Training',
    'Comprehensive leadership training program for student leaders covering communication skills, team management, and organizational development.',
    'LSPU Main Auditorium',
    CURRENT_DATE,
    '08:00:00',
    '20:00:00',
    100,
    '01234567-89ab-cdef-0123-456789abcdef', -- OSAS department_id
    'Active',
    NOW() - INTERVAL '5 days'
);

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'OSAS ongoing event created successfully!' as message;

-- Show the created event
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    participant_limit,
    status,
    created_at
FROM events 
WHERE department_id = '01234567-89ab-cdef-0123-456789abcdef'
    AND date = CURRENT_DATE
    AND status = 'Active'
ORDER BY created_at DESC
LIMIT 1;

-- ============================================
-- NOTES
-- ============================================
-- Event Details:
-- - Name: LSPU Student Leadership Training
-- - Date: TODAY (CURRENT_DATE)
-- - Time: 8:00 AM - 8:00 PM (20:00:00)
-- - Participant Limit: 100 (Limited Event)
-- - Status: Active (will show as "Ongoing" during event hours)
-- - Department: OSAS
--
-- Attendance Recording:
-- - When QR code is scanned, attended_at will be set to NOW()
-- - Supabase stores in UTC, but the controller converts to Philippine Time (UTC+8)
-- - Display format: "Dec 14, 2025 05:30 PM" (Philippine Time)
--
-- To Test:
-- 1. Run this script in Supabase SQL Editor
-- 2. Students register for the event
-- 3. OSAS approves registrations
-- 4. OSAS scans QR codes during event hours
-- 5. Check attendance report - time should be in Philippine Time
-- ============================================
