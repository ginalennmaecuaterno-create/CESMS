-- ============================================
-- FRESH START: CLEAN + ADD 22 ACTIVE EVENTS (2026)
-- This script will:
-- 1. Clean all event data
-- 2. Add 20 department events (Active, 2026)
-- 3. Add 2 OSAS events (Active, 2026)
-- Total: 22 Active Events
-- ============================================

BEGIN;

-- ============================================
-- STEP 1: CLEAN ALL EVENT DATA
-- ============================================

DELETE FROM event_feedback;
DELETE FROM event_requirements;
DELETE FROM attendance;
DELETE FROM event_registrations;
DELETE FROM events;
DELETE FROM event_requests;

-- ============================================
-- STEP 2: ADD 20 DEPARTMENT EVENTS (ACTIVE, 2026)
-- Direct insert to events table (no approval needed)
-- ============================================

-- COLLEGE OF AGRICULTURE (COA)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Sustainable Agriculture Forum', 'Open forum discussing sustainable farming practices and environmental conservation.', 'COA Auditorium', '2026-02-15', '09:00:00', '12:00:00', NULL, 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Active', NOW()),
(gen_random_uuid(), 'Hydroponics Workshop', 'Hands-on workshop on modern hydroponic farming techniques.', 'COA Greenhouse', '2026-02-17', '13:00:00', '17:00:00', 30, 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Active', NOW());

-- COLLEGE OF ARTS AND SCIENCES (CAS)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Science and Technology Expo', 'Exhibition showcasing student research projects and scientific innovations.', 'CAS Main Hall', '2026-02-18', '08:00:00', '17:00:00', NULL, 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Active', NOW()),
(gen_random_uuid(), 'Advanced Physics Laboratory Session', 'Exclusive laboratory session for advanced physics experiments.', 'CAS Physics Lab', '2026-02-20', '10:00:00', '15:00:00', 25, 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Active', NOW());

-- COLLEGE OF BUSINESS ADMINISTRATION AND ACCOUNTANCY (CBAA)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Entrepreneurship Summit 2026', 'Inspiring talks from successful entrepreneurs and business leaders.', 'CBAA Convention Center', '2026-02-21', '08:00:00', '16:00:00', NULL, 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Active', NOW()),
(gen_random_uuid(), 'Financial Analysis Masterclass', 'Intensive masterclass on financial statement analysis and investment strategies.', 'CBAA Seminar Room', '2026-02-24', '13:00:00', '17:00:00', 40, 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Active', NOW());

-- COLLEGE OF COMPUTER STUDIES (CCS)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Tech Talk: AI and Machine Learning', 'Informative session about artificial intelligence and machine learning trends.', 'CCS Auditorium', '2026-02-25', '14:00:00', '17:00:00', NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Active', NOW()),
(gen_random_uuid(), 'Cybersecurity Bootcamp', 'Intensive hands-on training on ethical hacking and cybersecurity.', 'CCS Security Lab', '2026-02-26', '09:00:00', '16:00:00', 35, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Active', NOW());

-- COLLEGE OF CRIMINAL JUSTICE EDUCATION (CCJE)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Law Enforcement Career Fair', 'Meet representatives from various law enforcement agencies.', 'CCJE Gymnasium', '2026-02-27', '09:00:00', '15:00:00', NULL, 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Active', NOW()),
(gen_random_uuid(), 'Forensic Investigation Workshop', 'Practical workshop on forensic evidence collection and analysis.', 'CCJE Forensics Lab', '2026-02-28', '13:00:00', '17:00:00', 30, 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Active', NOW());

-- COLLEGE OF FOOD NUTRITION AND DIETETICS (CFND)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Nutrition and Wellness Seminar', 'Educational seminar on proper nutrition and healthy lifestyle.', 'CFND Lecture Hall', '2026-03-03', '10:00:00', '13:00:00', NULL, 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Active', NOW()),
(gen_random_uuid(), 'Gourmet Cooking Class', 'Exclusive cooking class featuring gourmet techniques.', 'CFND Culinary Lab', '2026-03-04', '14:00:00', '18:00:00', 20, 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Active', NOW());

-- COLLEGE OF INTERNATIONAL HOSPITALITY AND TOURISM MANAGEMENT (CIHTM)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Tourism Industry Trends Forum', 'Discussion on current trends and future of tourism industry in the Philippines.', 'CIHTM Conference Room', '2026-03-05', '09:00:00', '12:00:00', NULL, 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Active', NOW()),
(gen_random_uuid(), 'Professional Bartending Course', 'Professional bartending training with certification.', 'CIHTM Bar Training Area', '2026-03-06', '13:00:00', '17:00:00', 25, 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Active', NOW());

-- COLLEGE OF INDUSTRIAL TECHNOLOGY (CIT)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Industrial Safety and Standards Seminar', 'Comprehensive seminar on workplace safety and industry standards.', 'CIT Main Hall', '2026-03-07', '08:00:00', '12:00:00', NULL, 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Active', NOW()),
(gen_random_uuid(), 'CNC Machining Workshop', 'Hands-on training on Computer Numerical Control machining.', 'CIT Machine Shop', '2026-03-10', '13:00:00', '17:00:00', 15, 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Active', NOW());

-- COLLEGE OF ENGINEERING (COE)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Engineering Innovation Showcase', 'Exhibition of innovative engineering projects and prototypes.', 'COE Exhibition Hall', '2026-03-11', '09:00:00', '16:00:00', NULL, 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Active', NOW()),
(gen_random_uuid(), 'Advanced CAD Design Workshop', 'Intensive workshop on advanced Computer-Aided Design techniques.', 'COE Design Lab', '2026-03-12', '10:00:00', '15:00:00', 30, 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Active', NOW());

-- COLLEGE OF TEACHER EDUCATION (CTE)
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Education Reform and Innovation Forum', 'Open forum discussing modern teaching methods and educational reforms.', 'CTE Auditorium', '2026-03-13', '08:00:00', '12:00:00', NULL, 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Active', NOW()),
(gen_random_uuid(), 'Interactive Teaching Methods Workshop', 'Practical workshop on interactive and engaging teaching strategies.', 'CTE Training Room', '2026-03-14', '13:00:00', '17:00:00', 35, 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Active', NOW());

-- ============================================
-- STEP 3: ADD 2 OSAS EVENTS (ACTIVE, 2026)
-- ============================================

INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'LSPU Foundation Day Celebration', 'University-wide celebration of LSPU Foundation Day with various activities and programs.', 'LSPU Main Quadrangle', '2026-03-17', '08:00:00', '17:00:00', NULL, '01234567-89ab-cdef-0123-456789abcdef', 'Active', NOW()),
(gen_random_uuid(), 'Student Leadership Summit', 'Exclusive leadership training summit for student organization officers and leaders.', 'LSPU Convention Center', '2026-03-18', '09:00:00', '16:00:00', 150, '01234567-89ab-cdef-0123-456789abcdef', 'Active', NOW());

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================

SELECT '22 Active Events created successfully!' as message;

-- Show all events
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
ORDER BY e.date, e.start_time;

-- Count by organizer
SELECT 
    CASE 
        WHEN u.role = 'osas' THEN 'OSAS'
        ELSE u.department_name
    END as organizer,
    COUNT(*) as event_count
FROM events e
JOIN users u ON e.department_id = u.id
GROUP BY organizer
ORDER BY organizer;

-- Total count
SELECT COUNT(*) as total_active_events
FROM events
WHERE status = 'Active';

-- ============================================
-- SUMMARY
-- ============================================
-- Total: 22 Active Events (2026 dates)
-- - 20 Department Events (2 per department)
-- - 2 OSAS Events
-- 
-- Event Types:
-- - 11 Free for All (unlimited)
-- - 11 Limited (15-150 slots)
--
-- Date Range: February 15 - March 18, 2026
-- All events are ACTIVE and ready for student registration!
-- ============================================
