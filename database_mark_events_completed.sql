-- ============================================
-- MARK ONGOING EVENTS AS COMPLETED
-- Updates only events that are currently happening (Ongoing) to Completed status
-- Leaves future Active events untouched
-- ============================================

BEGIN;

-- Update only Active events where current time is AFTER the end_time
-- This marks events that have already finished as Completed
UPDATE events
SET status = 'Completed'
WHERE status = 'Active'
  AND date = CURRENT_DATE
  AND CURRENT_TIME > end_time;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Ongoing/finished events marked as completed!' as message;

-- Show all events today with their time status
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    status,
    CASE 
        WHEN CURRENT_TIME < start_time THEN 'Future (Active)'
        WHEN CURRENT_TIME >= start_time AND CURRENT_TIME <= end_time THEN 'Currently Ongoing'
        WHEN CURRENT_TIME > end_time THEN 'Past (Should be Completed)'
    END as time_status
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
-- This script:
-- - Marks only events that have FINISHED (current time > end_time) as Completed
-- - Leaves future Active events untouched
-- - Leaves currently Ongoing events as Active (they will show as "Ongoing" via display_status)
-- - Allows students to see completed events in Event History
-- - Allows students to submit feedback for completed events
-- - Preserves all registrations and attendance data
--
-- To manually mark a specific ongoing event as completed:
-- UPDATE events SET status = 'Completed' WHERE id = 'event-id-here';
-- ============================================
