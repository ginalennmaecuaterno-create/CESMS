-- ============================================
-- UPDATE ALL EVENTS FROM 2025 TO 2026
-- This will make all completed events become active again
-- ============================================

BEGIN;

-- Update all events with 2025 dates to 2026
UPDATE events
SET date = date + INTERVAL '1 year'
WHERE EXTRACT(YEAR FROM date) = 2025;

-- Update all event_requests with 2025 dates to 2026
UPDATE event_requests
SET date = date + INTERVAL '1 year'
WHERE EXTRACT(YEAR FROM date) = 2025;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT 'All events updated to 2026!' as message;

-- Show all events (should now be Active with 2026 dates)
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    CASE WHEN participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || participant_limit || ')' END as event_type,
    status
FROM events 
ORDER BY date, start_time;

-- Count events by status
SELECT 
    status,
    COUNT(*) as count
FROM events
GROUP BY status;

-- Show total active events
SELECT COUNT(*) as total_active_events
FROM events
WHERE status = 'Active';

-- ============================================
-- SUMMARY
-- ============================================
-- All 2025 dates have been updated to 2026
-- Events that were "Completed" should now show as "Active"
-- (because they are now future dates)
-- ============================================
