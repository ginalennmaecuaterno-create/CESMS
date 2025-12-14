-- ============================================
-- ADD NEW ACTIVE EVENTS FOR ALL DEPARTMENTS
-- 2 events per department (1 Free for All, 1 Limited)
-- Different dates to avoid conflicts
-- ============================================

BEGIN;

-- ============================================
-- COLLEGE OF AGRICULTURE (COA)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Sustainable Agriculture Forum', 'Open forum discussing sustainable farming practices and environmental conservation in agriculture.', 'COA Auditorium', '2025-01-20', '09:00:00', '12:00:00', NULL, 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Hydroponics Workshop', 'Hands-on workshop on modern hydroponic farming techniques with limited slots for practical training.', 'COA Greenhouse', '2025-01-22', '13:00:00', '17:00:00', 30, 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Active', NOW());

-- ============================================
-- COLLEGE OF ARTS AND SCIENCES (CAS)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Science and Technology Expo', 'Exhibition showcasing student research projects and scientific innovations. Open to all students.', 'CAS Main Hall', '2025-01-21', '08:00:00', '17:00:00', NULL, 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Advanced Physics Laboratory Session', 'Exclusive laboratory session for advanced physics experiments with limited equipment slots.', 'CAS Physics Lab', '2025-01-23', '10:00:00', '15:00:00', 25, 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Active', NOW());

-- ============================================
-- COLLEGE OF BUSINESS ADMINISTRATION AND ACCOUNTANCY (CBAA)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Entrepreneurship Summit 2025', 'Inspiring talks from successful entrepreneurs and business leaders. Free admission for all students.', 'CBAA Convention Center', '2025-01-24', '08:00:00', '16:00:00', NULL, 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Financial Analysis Masterclass', 'Intensive masterclass on financial statement analysis and investment strategies with limited seats.', 'CBAA Seminar Room', '2025-01-25', '13:00:00', '17:00:00', 40, 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Active', NOW());

-- ============================================
-- COLLEGE OF COMPUTER STUDIES (CCS)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Tech Talk: AI and Machine Learning', 'Informative session about artificial intelligence and machine learning trends. Open to all interested students.', 'CCS Auditorium', '2025-01-27', '14:00:00', '17:00:00', NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Cybersecurity Bootcamp', 'Intensive hands-on training on ethical hacking and cybersecurity with limited lab computers.', 'CCS Security Lab', '2025-01-28', '09:00:00', '16:00:00', 35, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Active', NOW());

-- ============================================
-- COLLEGE OF CRIMINAL JUSTICE EDUCATION (CCJE)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Law Enforcement Career Fair', 'Meet representatives from various law enforcement agencies. Open to all students interested in criminal justice careers.', 'CCJE Gymnasium', '2025-01-29', '09:00:00', '15:00:00', NULL, 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Forensic Investigation Workshop', 'Practical workshop on forensic evidence collection and analysis with limited equipment and materials.', 'CCJE Forensics Lab', '2025-01-30', '13:00:00', '17:00:00', 30, 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Active', NOW());

-- ============================================
-- COLLEGE OF FOOD NUTRITION AND DIETETICS (CFND)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Nutrition and Wellness Seminar', 'Educational seminar on proper nutrition and healthy lifestyle. Free and open to all students.', 'CFND Lecture Hall', '2025-01-31', '10:00:00', '13:00:00', NULL, 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Gourmet Cooking Class', 'Exclusive cooking class featuring gourmet techniques with limited kitchen stations.', 'CFND Culinary Lab', '2025-02-03', '14:00:00', '18:00:00', 20, 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Active', NOW());

-- ============================================
-- COLLEGE OF INTERNATIONAL HOSPITALITY AND TOURISM MANAGEMENT (CIHTM)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Tourism Industry Trends Forum', 'Discussion on current trends and future of tourism industry in the Philippines. Open to all.', 'CIHTM Conference Room', '2025-02-04', '09:00:00', '12:00:00', NULL, 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Professional Bartending Course', 'Professional bartending training with certification. Limited slots due to equipment availability.', 'CIHTM Bar Training Area', '2025-02-05', '13:00:00', '17:00:00', 25, 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Active', NOW());

-- ============================================
-- COLLEGE OF INDUSTRIAL TECHNOLOGY (CIT)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Industrial Safety and Standards Seminar', 'Comprehensive seminar on workplace safety and industry standards. Free admission for all students.', 'CIT Main Hall', '2025-02-06', '08:00:00', '12:00:00', NULL, 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'CNC Machining Workshop', 'Hands-on training on Computer Numerical Control machining with limited machine access.', 'CIT Machine Shop', '2025-02-07', '13:00:00', '17:00:00', 15, 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Active', NOW());

-- ============================================
-- COLLEGE OF ENGINEERING (COE)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Engineering Innovation Showcase', 'Exhibition of innovative engineering projects and prototypes. Open to all students and faculty.', 'COE Exhibition Hall', '2025-02-10', '09:00:00', '16:00:00', NULL, 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Advanced CAD Design Workshop', 'Intensive workshop on advanced Computer-Aided Design techniques with limited workstations.', 'COE Design Lab', '2025-02-11', '10:00:00', '15:00:00', 30, 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Active', NOW());

-- ============================================
-- COLLEGE OF TEACHER EDUCATION (CTE)
-- ============================================

-- Free for All Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Education Reform and Innovation Forum', 'Open forum discussing modern teaching methods and educational reforms. Free for all attendees.', 'CTE Auditorium', '2025-02-12', '08:00:00', '12:00:00', NULL, 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Active', NOW());

-- Limited Event
INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'Interactive Teaching Methods Workshop', 'Practical workshop on interactive and engaging teaching strategies with limited participant slots.', 'CTE Training Room', '2025-02-13', '13:00:00', '17:00:00', 35, 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Active', NOW());

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'New active events created successfully!' as message;

-- Show all new events
SELECT 
    event_name,
    date,
    start_time,
    end_time,
    CASE WHEN participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || participant_limit || ')' END as event_type,
    status
FROM events 
WHERE date >= '2025-01-20'
ORDER BY date, start_time;

-- Count by department
SELECT 
    u.department_name,
    COUNT(*) as event_count
FROM events e
JOIN users u ON e.department_id = u.id
WHERE e.date >= '2025-01-20'
GROUP BY u.department_name
ORDER BY u.department_name;

-- ============================================
-- SUMMARY
-- ============================================
-- Total Events Created: 20 (2 per department × 10 departments)
-- - 10 Free for All events (no participant limit)
-- - 10 Limited events (with participant limits)
--
-- Date Range: January 20 - February 13, 2025
-- All events scheduled at different dates to avoid conflicts
--
-- Event Types:
-- - Free for All: Open to unlimited students
-- - Limited: Requires approval, has participant limits
-- ============================================
