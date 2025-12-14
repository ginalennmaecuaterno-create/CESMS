-- ============================================
-- FIX ALL EVENTS TO ACTIVE STATUS
-- Remove duplicates and set all to Active
-- ============================================

BEGIN;

-- Step 1: Delete duplicate events (keep only unique event names per department)
DELETE FROM events
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY event_name, department_id ORDER BY created_at) as rn
        FROM events
    ) t
    WHERE rn > 1
);

-- Step 2: Update ALL remaining events to Active status
UPDATE events
SET status = 'Active'
WHERE date >= CURRENT_DATE;

-- Step 3: Delete any events that are still in the past (just in case)
DELETE FROM events
WHERE date < CURRENT_DATE;

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT 'All events fixed!' as message;

-- Show all events (should be 22 Active events)
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    CASE WHEN participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || participant_limit || ')' END as event_type,
    status,
    CASE 
        WHEN u.role = 'osas' THEN 'OSAS'
        ELSE u.department_name
    END as organizer
FROM events e
JOIN users u ON e.department_id = u.id
ORDER BY date, start_time;

-- Count by status
SELECT 
    status,
    COUNT(*) as count
FROM events
GROUP BY status;

-- Total count
SELECT COUNT(*) as total_events FROM events;

-- ============================================
-- EXPECTED RESULT: 22 Active Events
-- - 20 Department events (2 per department)
-- - 2 OSAS events
-- ============================================
