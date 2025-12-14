-- ============================================
-- ADD EVENT REQUESTS FOR ALL DEPARTMENTS
-- 2 requests per department (1 Free for All, 1 Limited)
-- Status: Pending (needs OSAS approval)
-- ============================================

BEGIN;

-- ============================================
-- COLLEGE OF AGRICULTURE (COA)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Sustainable Agriculture Forum', 'Open forum discussing sustainable farming practices and environmental conservation in agriculture.', 'COA Auditorium', '2025-01-20', '09:00:00', '12:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Hydroponics Workshop', 'Hands-on workshop on modern hydroponic farming techniques with limited slots for practical training.', 'COA Greenhouse', '2025-01-22', '13:00:00', '17:00:00', 30, 'Pending', NOW());

-- ============================================
-- COLLEGE OF ARTS AND SCIENCES (CAS)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Science and Technology Expo', 'Exhibition showcasing student research projects and scientific innovations. Open to all students.', 'CAS Main Hall', '2025-01-21', '08:00:00', '17:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Advanced Physics Laboratory Session', 'Exclusive laboratory session for advanced physics experiments with limited equipment slots.', 'CAS Physics Lab', '2025-01-23', '10:00:00', '15:00:00', 25, 'Pending', NOW());

-- ============================================
-- COLLEGE OF BUSINESS ADMINISTRATION AND ACCOUNTANCY (CBAA)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Entrepreneurship Summit 2025', 'Inspiring talks from successful entrepreneurs and business leaders. Free admission for all students.', 'CBAA Convention Center', '2025-01-24', '08:00:00', '16:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Financial Analysis Masterclass', 'Intensive masterclass on financial statement analysis and investment strategies with limited seats.', 'CBAA Seminar Room', '2025-01-25', '13:00:00', '17:00:00', 40, 'Pending', NOW());

-- ============================================
-- COLLEGE OF COMPUTER STUDIES (CCS)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Tech Talk: AI and Machine Learning', 'Informative session about artificial intelligence and machine learning trends. Open to all interested students.', 'CCS Auditorium', '2025-01-27', '14:00:00', '17:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Cybersecurity Bootcamp', 'Intensive hands-on training on ethical hacking and cybersecurity with limited lab computers.', 'CCS Security Lab', '2025-01-28', '09:00:00', '16:00:00', 35, 'Pending', NOW());

-- ============================================
-- COLLEGE OF CRIMINAL JUSTICE EDUCATION (CCJE)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Law Enforcement Career Fair', 'Meet representatives from various law enforcement agencies. Open to all students interested in criminal justice careers.', 'CCJE Gymnasium', '2025-01-29', '09:00:00', '15:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Forensic Investigation Workshop', 'Practical workshop on forensic evidence collection and analysis with limited equipment and materials.', 'CCJE Forensics Lab', '2025-01-30', '13:00:00', '17:00:00', 30, 'Pending', NOW());

-- ============================================
-- COLLEGE OF FOOD NUTRITION AND DIETETICS (CFND)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Nutrition and Wellness Seminar', 'Educational seminar on proper nutrition and healthy lifestyle. Free and open to all students.', 'CFND Lecture Hall', '2025-01-31', '10:00:00', '13:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Gourmet Cooking Class', 'Exclusive cooking class featuring gourmet techniques with limited kitchen stations.', 'CFND Culinary Lab', '2025-02-03', '14:00:00', '18:00:00', 20, 'Pending', NOW());

-- ============================================
-- COLLEGE OF INTERNATIONAL HOSPITALITY AND TOURISM MANAGEMENT (CIHTM)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Tourism Industry Trends Forum', 'Discussion on current trends and future of tourism industry in the Philippines. Open to all.', 'CIHTM Conference Room', '2025-02-04', '09:00:00', '12:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Professional Bartending Course', 'Professional bartending training with certification. Limited slots due to equipment availability.', 'CIHTM Bar Training Area', '2025-02-05', '13:00:00', '17:00:00', 25, 'Pending', NOW());

-- ============================================
-- COLLEGE OF INDUSTRIAL TECHNOLOGY (CIT)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Industrial Safety and Standards Seminar', 'Comprehensive seminar on workplace safety and industry standards. Free admission for all students.', 'CIT Main Hall', '2025-02-06', '08:00:00', '12:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'CNC Machining Workshop', 'Hands-on training on Computer Numerical Control machining with limited machine access.', 'CIT Machine Shop', '2025-02-07', '13:00:00', '17:00:00', 15, 'Pending', NOW());

-- ============================================
-- COLLEGE OF ENGINEERING (COE)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Engineering Innovation Showcase', 'Exhibition of innovative engineering projects and prototypes. Open to all students and faculty.', 'COE Exhibition Hall', '2025-02-10', '09:00:00', '16:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Advanced CAD Design Workshop', 'Intensive workshop on advanced Computer-Aided Design techniques with limited workstations.', 'COE Design Lab', '2025-02-11', '10:00:00', '15:00:00', 30, 'Pending', NOW());

-- ============================================
-- COLLEGE OF TEACHER EDUCATION (CTE)
-- ============================================

INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at) VALUES
(gen_random_uuid(), 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Education Reform and Innovation Forum', 'Open forum discussing modern teaching methods and educational reforms. Free for all attendees.', 'CTE Auditorium', '2025-02-12', '08:00:00', '12:00:00', NULL, 'Pending', NOW()),
(gen_random_uuid(), 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Interactive Teaching Methods Workshop', 'Practical workshop on interactive and engaging teaching strategies with limited participant slots.', 'CTE Training Room', '2025-02-13', '13:00:00', '17:00:00', 35, 'Pending', NOW());

COMMIT;

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Event requests created successfully!' as message;
SELECT 'OSAS needs to approve these requests before they appear in Browse Events' as note;

-- Show all new requests
SELECT 
    er.event_name,
    er.date,
    er.start_time,
    er.end_time,
    CASE WHEN er.participant_limit IS NULL THEN 'Free for All' ELSE 'Limited (' || er.participant_limit || ')' END as event_type,
    er.status,
    u.department_name
FROM event_requests er
JOIN users u ON er.department_id = u.id
WHERE er.created_at >= NOW() - INTERVAL '1 minute'
ORDER BY er.date, er.start_time;

-- ============================================
-- NEXT STEPS
-- ============================================
-- 1. Login as OSAS
-- 2. Go to Event Request Management
-- 3. Approve these 20 pending requests
-- 4. Events will then appear in Browse Events page for students
-- ============================================
