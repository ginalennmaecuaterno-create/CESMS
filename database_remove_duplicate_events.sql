-- ============================================
-- REMOVE DUPLICATE ONGOING EVENTS
-- Keeps only the oldest entry for each event name
-- ============================================

BEGIN;

-- Delete duplicate events (keep only the first created one)
DELETE FROM events
WHERE id IN (
    SELECT id
    FROM (
        SELECT 
            id,
            event_name,
            ROW_NUMBER() OVER (PARTITION BY event_name ORDER BY created_at ASC) as rn
        FROM events
        WHERE status = 'Active' 
            AND date = CURRENT_DATE
    ) t
    WHERE rn > 1
);

COMMIT;

-- Verify results
SELECT 'Duplicates removed!' as message;
SELECT 
    COUNT(*) as remaining_active_events
FROM events 
WHERE status = 'Active' 
    AND date = CURRENT_DATE;

-- Show remaining events
SELECT 
    event_name,
    date,
    status,
    participant_limit
FROM events 
WHERE status = 'Active' 
    AND date = CURRENT_DATE
ORDER BY event_name;
