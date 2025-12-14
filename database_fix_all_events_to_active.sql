-- ============================================
-- FIX: REVERT ALL FUTURE EVENTS TO ACTIVE
-- Changes all Completed events with future dates back to Active
-- ============================================

BEGIN;

-- Update all events with future dates (after today) to Active
UPDATE events
SET status = 'Active'
WHERE status = 'Completed'
  AND date > CURRENT_DATE;

-- Also update events today that haven't started yet
UPDATE events
SET status = 'Active'
WHERE status = 'Completed'
  AND date = CURRENT_DATE
  AND CURRENT_TIME < start_time;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Events fixed! Future events are now Active.' as message;

-- Show all events by status
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    status,
    CASE 
        WHEN date > CURRENT_DATE THEN 'Future Event'
        WHEN date = CURRENT_DATE AND CURRENT_TIME < start_time THEN 'Today (Not Started)'
        WHEN date = CURRENT_DATE AND CURRENT_TIME >= start_time AND CURRENT_TIME <= end_time THEN 'Ongoing Now'
        WHEN date = CURRENT_DATE AND CURRENT_TIME > end_time THEN 'Today (Finished)'
        ELSE 'Past Event'
    END as time_status
FROM events 
WHERE date >= CURRENT_DATE
ORDER BY date, start_time;

-- Count by status
SELECT 
    status,
    COUNT(*) as count
FROM events
WHERE date >= CURRENT_DATE
GROUP BY status
ORDER BY status;

-- ============================================
-- SUMMARY
-- ============================================
-- This script:
-- - Changes all future events (date > today) to Active
-- - Changes today's events that haven't started yet to Active
-- - Leaves past/finished events as Completed
-- - Events will now appear in Browse Events page
-- ============================================
