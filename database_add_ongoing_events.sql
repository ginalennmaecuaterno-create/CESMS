-- ============================================
-- ADD ONGOING EVENTS FOR ATTENDANCE TESTING
-- 1 Completed OSAS Event
-- 1 Active Limited Event per Department (10 total)
-- ============================================

BEGIN;

-- ============================================
-- OSAS COMPLETED EVENT
-- ============================================

INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'LSPU Orientation Day 2025', 'Welcome orientation for all new students with campus tour and introduction to university services.', 'LSPU Gymnasium', '2025-01-15', '08:00:00', '17:00:00', NULL, '01234567-89ab-cdef-0123-456789abcdef', 'Completed', NOW() - INTERVAL '30 days');

-- ============================================
-- DEPARTMENT ONGOING EVENTS (Active, Limited, Happening Today/This Week)
-- Perfect for testing attendance scanning
-- ============================================

-- College of Agriculture - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Organic Farming Workshop', 'Hands-on workshop on organic farming techniques and sustainable agriculture practices.', 'COA Demo Farm', CURRENT_DATE, '08:00:00', '20:00:00', 50, 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Active', NOW() - INTERVAL '7 days');

-- College of Arts and Sciences - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Research Symposium', 'Student research presentations and poster sessions across various scientific disciplines.', 'CAS Auditorium', CURRENT_DATE, '09:00:00', '20:00:00', 100, 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Active', NOW() - INTERVAL '5 days');

-- College of Business Administration and Accountancy - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Business Plan Competition', 'Students pitch their business ideas to a panel of judges and investors.', 'CBAA Conference Room', CURRENT_DATE, '08:00:00', '20:00:00', 60, 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Active', NOW() - INTERVAL '10 days');

-- College of Computer Studies - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Programming Workshop: Python Basics', 'Introduction to Python programming for beginners with hands-on coding exercises.', 'CCS Computer Lab 1', CURRENT_DATE, '13:00:00', '20:00:00', 40, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Active', NOW() - INTERVAL '3 days');

-- College of Criminal Justice Education - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Crime Scene Investigation Training', 'Practical training on crime scene processing and evidence collection techniques.', 'CCJE Training Ground', CURRENT_DATE, '08:00:00', '20:00:00', 80, 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Active', NOW() - INTERVAL '6 days');

-- College of Engineering - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Robotics Workshop', 'Build and program your own robot using Arduino and sensors.', 'COE Robotics Lab', CURRENT_DATE, '09:00:00', '20:00:00', 50, 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Active', NOW() - INTERVAL '8 days');

-- College of Food Nutrition and Dietetics - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Culinary Arts Competition', 'Students showcase their culinary skills in a timed cooking competition.', 'CFND Culinary Lab', CURRENT_DATE, '10:00:00', '20:00:00', 30, 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Active', NOW() - INTERVAL '4 days');

-- College of Industrial Technology - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Welding and Fabrication Workshop', 'Learn basic welding techniques and metal fabrication skills.', 'CIT Workshop', CURRENT_DATE, '08:00:00', '20:00:00', 45, 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Active', NOW() - INTERVAL '9 days');

-- College of International Hospitality and Tourism Management - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Barista Training Workshop', 'Professional barista training covering coffee preparation and latte art.', 'CIHTM Training Kitchen', CURRENT_DATE, '13:00:00', '20:00:00', 35, 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Active', NOW() - INTERVAL '2 days');

-- College of Teacher Education - Ongoing Today
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Classroom Management Seminar', 'Learn effective strategies for managing diverse classrooms and student behavior.', 'CTE Training Room', CURRENT_DATE, '09:00:00', '20:00:00', 70, 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Active', NOW() - INTERVAL '5 days');

COMMIT;

-- ============================================
-- SUMMARY
-- ============================================
-- Total Events Created: 11
-- - 1 OSAS Completed Event (for history testing)
-- - 10 Department Active Events (1 per department, all happening TODAY)
--
-- All active events:
-- - Have participant limits (Limited Events)
-- - Are scheduled for TODAY (CURRENT_DATE)
-- - Have status 'Active'
-- - Perfect for testing QR code attendance scanning
--
-- To test attendance:
-- 1. Students register for these events
-- 2. Departments/OSAS can scan QR codes to mark attendance
-- 3. Check attendance reports
-- ============================================

SELECT 'Ongoing events created successfully!' as message;
SELECT 'All department events are happening TODAY - perfect for attendance testing!' as info;
SELECT COUNT(*) as total_active_events FROM events WHERE status = 'Active' AND date = CURRENT_DATE;
SELECT COUNT(*) as total_completed_events FROM events WHERE status = 'Completed';
