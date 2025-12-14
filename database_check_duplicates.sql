-- ============================================
-- CHECK FOR DUPLICATE ONGOING EVENTS
-- ============================================

-- Check all active events happening today
SELECT 
    event_name,
    date,
    status,
    participant_limit,
    created_at
FROM events 
WHERE status = 'Active' 
    AND date = CURRENT_DATE
ORDER BY event_name, created_at;

-- Count duplicates
SELECT 
    event_name,
    COUNT(*) as count
FROM events 
WHERE status = 'Active' 
    AND date = CURRENT_DATE
GROUP BY event_name
HAVING COUNT(*) > 1;

-- Total count
SELECT 
    COUNT(*) as total_active_today
FROM events 
WHERE status = 'Active' 
    AND date = CURRENT_DATE;
