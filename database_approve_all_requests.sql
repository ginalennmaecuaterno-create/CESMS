-- ============================================
-- APPROVE ALL PENDING EVENT REQUESTS
-- Simulates OSAS approving all department event requests
-- ============================================

BEGIN;

-- ============================================
-- STEP 1: Move all pending requests to events table
-- ============================================

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
)
SELECT 
    gen_random_uuid(),  -- Generate new ID for events table
    event_name,
    description,
    location,
    date,
    start_time,
    end_time,
    participant_limit,
    department_id,
    'Active',  -- Set status to Active (approved)
    NOW()  -- Set created_at to current timestamp
FROM event_requests
WHERE status = 'Pending';

-- ============================================
-- STEP 2: Update event_requests status to Approved
-- ============================================

UPDATE event_requests
SET status = 'Approved'
WHERE status = 'Pending';

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT 'All event requests approved successfully!' as message;

-- Show all approved requests
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    CASE WHEN participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || participant_limit || ')' END as event_type,
    status
FROM event_requests 
WHERE status = 'Approved'
ORDER BY date, start_time;

-- Show all active events (should now include approved department events + OSAS events)
SELECT 
    e.event_name,
    e.date,
    e.start_time,
    e.end_time,
    CASE WHEN e.participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || e.participant_limit || ')' END as event_type,
    e.status,
    CASE 
        WHEN u.role = 'osas' THEN 'OSAS'
        ELSE u.department_name
    END as organizer
FROM events e
JOIN users u ON e.department_id = u.id
WHERE e.status = 'Active'
ORDER BY e.date, e.start_time;

-- Count active events by organizer
SELECT 
    CASE 
        WHEN u.role = 'osas' THEN 'OSAS'
        ELSE u.department_name
    END as organizer,
    COUNT(*) as active_events
FROM events e
JOIN users u ON e.department_id = u.id
WHERE e.status = 'Active'
GROUP BY organizer
ORDER BY organizer;

-- ============================================
-- SUMMARY
-- ============================================
-- All 20 department event requests have been approved!
--
-- BEFORE:
-- - event_requests: 20 Pending
-- - events: 2 Active (OSAS only)
--
-- AFTER:
-- - event_requests: 20 Approved (archived)
-- - events: 22 Active (20 department + 2 OSAS)
--
-- Students can now:
-- - Browse all 22 events
-- - Register for any event
-- - View event details
--
-- Departments can now:
-- - Manage their approved events
-- - View registrations
-- - Scan QR codes for attendance
-- ============================================
