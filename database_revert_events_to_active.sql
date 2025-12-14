-- ============================================
-- REVERT COMPLETED EVENTS BACK TO ACTIVE
-- Changes all Completed events happening today back to Active status
-- ============================================

BEGIN;

-- Update all Completed events that are happening today back to Active
UPDATE events
SET status = 'Active'
WHERE status = 'Completed'
  AND date = CURRENT_DATE;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Events reverted to Active!' as message;

-- Show updated events
SELECT 
    event_name,
    date,
    status,
    department_id
FROM events 
WHERE date = CURRENT_DATE
ORDER BY event_name;

-- Count by status
SELECT 
    status,
    COUNT(*) as count
FROM events
GROUP BY status
ORDER BY status;

-- ============================================
-- NOTES
-- ============================================
-- This script:
-- - Reverts all Completed events happening TODAY back to Active
-- - Makes them visible again in Browse Events page
-- - Allows students to register again
-- - Preserves all existing registrations and attendance data
--
-- Events will show as:
-- - "Active" if before event time
-- - "Ongoing" if during event time
-- - "Completed" if after event time (automatically by display_status logic)
-- ============================================
