-- ============================================
-- MANUALLY MARK CURRENTLY ONGOING EVENTS AS COMPLETED
-- For testing purposes - marks events that are currently happening
-- ============================================

BEGIN;

-- Update Active events where current time is BETWEEN start_time and end_time
-- This marks currently ongoing events as Completed (for testing)
UPDATE events
SET status = 'Completed'
WHERE status = 'Active'
  AND date = CURRENT_DATE
  AND CURRENT_TIME >= start_time
  AND CURRENT_TIME <= end_time;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Currently ongoing events marked as completed!' as message;

-- Show all events today with their status
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    status,
    CASE 
        WHEN CURRENT_TIME < start_time THEN 'Future (Not yet started)'
        WHEN CURRENT_TIME >= start_time AND CURRENT_TIME <= end_time THEN 'Currently Ongoing'
        WHEN CURRENT_TIME > end_time THEN 'Past (Already finished)'
    END as time_status,
    CURRENT_TIME as current_time
FROM events 
WHERE date = CURRENT_DATE
ORDER BY start_time;

-- Count by status
SELECT 
    status,
    COUNT(*) as count
FROM events
WHERE date = CURRENT_DATE
GROUP BY status
ORDER BY status;

-- ============================================
-- NOTES
-- ============================================
-- This script is for TESTING purposes:
-- - Marks events that are CURRENTLY HAPPENING (ongoing) as Completed
-- - Leaves future Active events untouched
-- - Allows you to test Event History and Feedback features
-- - Preserves all registrations and attendance data
--
-- Use this when you want to test completed events functionality
-- without waiting for events to actually finish
--
-- To revert back to Active:
-- UPDATE events SET status = 'Active' WHERE date = CURRENT_DATE AND status = 'Completed';
-- ============================================
