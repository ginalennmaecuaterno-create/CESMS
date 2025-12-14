-- ============================================
-- ADJUST EVENT END TIMES TO MAKE THEM COMPLETED
-- Changes end_time to 1 hour ago so events become "Completed"
-- ============================================

BEGIN;

-- Update end_time of Active events happening today to 1 hour ago
-- This makes them automatically show as "Completed" via display_status logic
UPDATE events
SET end_time = (CURRENT_TIME - INTERVAL '1 hour')::time
WHERE status = 'Active'
  AND date = CURRENT_DATE
  AND CURRENT_TIME >= start_time;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Event times adjusted!' as message;

-- Show all events today with their updated times
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    status,
    CASE 
        WHEN CURRENT_TIME < start_time THEN 'Future (Active)'
        WHEN CURRENT_TIME >= start_time AND CURRENT_TIME <= end_time THEN 'Currently Ongoing'
        WHEN CURRENT_TIME > end_time THEN 'Past (Completed)'
    END as display_status,
    CURRENT_TIME as current_time
FROM events 
WHERE date = CURRENT_DATE
ORDER BY start_time;

-- ============================================
-- NOTES
-- ============================================
-- This script:
-- - Changes end_time to 1 hour ago for events that have started
-- - Makes them automatically show as "Completed" (via display_status logic)
-- - No need to change status in database
-- - Events will appear in Event History
-- - Students can submit feedback
--
-- The system automatically calculates display_status based on:
-- - If current_time > end_time → "Completed"
-- - If current_time between start_time and end_time → "Ongoing"
-- - If current_time < start_time → "Active"
-- ============================================
