-- ============================================
-- ADD SAMPLE EVENTS
-- 2 Event Requests per Department (1 Limited, 1 Free for All)
-- 2 OSAS Events (1 Limited, 1 Free for All)
-- ============================================

BEGIN;

-- ============================================
-- DEPARTMENT EVENT REQUESTS
-- ============================================

-- College of Agriculture
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Agricultural Innovation Summit', 'Explore the latest innovations in sustainable farming and agricultural technology.', 'Agriculture Building Auditorium', '2025-02-15', '09:00:00', '16:00:00', 100, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Registration Form", "description": "Completed event registration form"}]'),
(gen_random_uuid(), 'd1a2b3c4-e5f6-7890-abcd-ef1234567891', 'Farm-to-Table Workshop', 'Learn about organic farming practices and sustainable food production.', 'COA Demo Farm', '2025-02-20', '13:00:00', '17:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Arts and Sciences
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Science and Arts Festival', 'A celebration of creativity and scientific discovery through interactive exhibits.', 'CAS Main Hall', '2025-02-18', '08:00:00', '17:00:00', 150, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Waiver Form", "description": "Signed participation waiver"}]'),
(gen_random_uuid(), 'd2a2b3c4-e5f6-7890-abcd-ef1234567892', 'Literary Reading Session', 'An open forum for students to share their creative writing and poetry.', 'CAS Library', '2025-02-22', '14:00:00', '16:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Business Administration and Accountancy
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Entrepreneurship Bootcamp', 'Intensive training on starting and managing your own business venture.', 'CBAA Conference Room', '2025-02-16', '08:00:00', '17:00:00', 80, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Business Plan Draft", "description": "Initial business concept or plan"}]'),
(gen_random_uuid(), 'd3a2b3c4-e5f6-7890-abcd-ef1234567893', 'Financial Literacy Seminar', 'Learn essential money management skills for students and young professionals.', 'CBAA Auditorium', '2025-02-25', '13:00:00', '16:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Computer Studies
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Hackathon 2025', '24-hour coding competition to build innovative tech solutions.', 'CCS Computer Laboratory', '2025-02-17', '08:00:00', '08:00:00', 50, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Laptop", "description": "Personal laptop for coding"}, {"name": "Team Registration", "description": "Team of 3-5 members"}]'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Web Development Workshop', 'Hands-on workshop on modern web development frameworks and best practices.', 'CCS Lecture Hall', '2025-02-28', '09:00:00', '17:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Criminal Justice Education
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Law Enforcement Career Fair', 'Meet with representatives from various law enforcement agencies and learn about career opportunities.', 'CCJE Gymnasium', '2025-02-19', '09:00:00', '15:00:00', 120, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Resume", "description": "Updated resume or CV"}]'),
(gen_random_uuid(), 'd4a2b3c4-e5f6-7890-abcd-ef1234567894', 'Criminology Lecture Series', 'Guest speakers discuss current trends and issues in criminal justice.', 'CCJE Auditorium', '2025-02-26', '14:00:00', '17:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Engineering
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Engineering Design Competition', 'Showcase your engineering skills by designing innovative solutions to real-world problems.', 'COE Workshop', '2025-02-21', '08:00:00', '18:00:00', 60, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Project Proposal", "description": "Detailed project proposal and design"}, {"name": "Team Registration", "description": "Team of 4-6 members"}]'),
(gen_random_uuid(), 'd8a2b3c4-e5f6-7890-abcd-ef1234567898', 'Sustainable Engineering Forum', 'Discussion on sustainable practices in engineering and construction.', 'COE Auditorium', '2025-03-01', '13:00:00', '16:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Food Nutrition and Dietetics
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Healthy Cooking Masterclass', 'Learn to prepare nutritious and delicious meals with professional chefs.', 'CFND Culinary Lab', '2025-02-23', '10:00:00', '15:00:00', 40, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Apron and Chef Hat", "description": "Personal cooking attire"}]'),
(gen_random_uuid(), 'd5a2b3c4-e5f6-7890-abcd-ef1234567895', 'Nutrition Awareness Campaign', 'Community outreach program promoting healthy eating habits.', 'CFND Main Building', '2025-02-27', '08:00:00', '12:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Industrial Technology
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Industrial Automation Workshop', 'Hands-on training on modern automation systems and robotics.', 'CIT Laboratory', '2025-02-24', '09:00:00', '17:00:00', 50, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Safety Gear", "description": "Personal protective equipment"}]'),
(gen_random_uuid(), 'd7a2b3c4-e5f6-7890-abcd-ef1234567897', 'Manufacturing Technology Seminar', 'Explore the latest trends in manufacturing and production technology.', 'CIT Conference Hall', '2025-03-03', '13:00:00', '16:00:00', NULL, 'Pending', NOW(), NULL);

-- College of International Hospitality and Tourism Management
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Hotel Management Training', 'Professional training on hotel operations and guest services.', 'CIHTM Training Center', '2025-02-25', '08:00:00', '17:00:00', 70, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Professional Attire", "description": "Business formal dress code"}]'),
(gen_random_uuid(), 'd6a2b3c4-e5f6-7890-abcd-ef1234567896', 'Tourism and Culture Festival', 'Celebrate Philippine tourism and cultural heritage through exhibits and performances.', 'CIHTM Courtyard', '2025-03-05', '10:00:00', '18:00:00', NULL, 'Pending', NOW(), NULL);

-- College of Teacher Education
INSERT INTO event_requests (id, department_id, event_name, description, location, date, start_time, end_time, participant_limit, status, created_at, requirements) VALUES
(gen_random_uuid(), 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Teaching Methodologies Workshop', 'Learn innovative teaching strategies and classroom management techniques.', 'CTE Training Room', '2025-02-26', '08:00:00', '16:00:00', 90, 'Pending', NOW(), '[{"name": "Student ID", "description": "Valid student identification"}, {"name": "Teaching Portfolio", "description": "Sample lesson plans or teaching materials"}]'),
(gen_random_uuid(), 'd9a2b3c4-e5f6-7890-abcd-ef1234567899', 'Education Summit', 'Forum on the future of education and educational reforms in the Philippines.', 'CTE Auditorium', '2025-03-07', '09:00:00', '17:00:00', NULL, 'Pending', NOW(), NULL);

-- ============================================
-- OSAS EVENTS (Direct to events table)
-- ============================================

INSERT INTO events (id, event_name, description, location, date, start_time, end_time, participant_limit, department_id, status, created_at) VALUES
(gen_random_uuid(), 'LSPU Foundation Day Celebration', 'Annual celebration of LSPU''s founding with cultural performances, competitions, and exhibits.', 'LSPU Main Quadrangle', '2025-03-10', '07:00:00', '18:00:00', 500, '01234567-89ab-cdef-0123-456789abcdef', 'Active', NOW()),
(gen_random_uuid(), 'Student Leadership Summit', 'Open forum for all students to develop leadership skills and network with student leaders.', 'OSAS Conference Hall', '2025-03-15', '08:00:00', '17:00:00', NULL, '01234567-89ab-cdef-0123-456789abcdef', 'Active', NOW());

COMMIT;

-- ============================================
-- SUMMARY
-- ============================================
-- Total Event Requests Created: 20 (2 per department x 10 departments)
-- - 10 Limited Events (with participant limits and requirements)
-- - 10 Free for All Events (no participant limits)
--
-- Total OSAS Events Created: 2
-- - 1 Limited Event (500 participants)
-- - 1 Free for All Event (unlimited)
--
-- All events are scheduled for February-March 2025
-- All department event requests have status 'Pending' (waiting for OSAS approval)
-- All OSAS events have status 'Active' (already live and accepting registrations)
-- ============================================

SELECT 'Sample events created successfully!' as message;
SELECT COUNT(*) as total_event_requests FROM event_requests;
SELECT COUNT(*) as total_osas_events FROM events WHERE department_id = '01234567-89ab-cdef-0123-456789abcdef';
