-- Create Department Accounts for All Colleges
-- Password for all: lspudept123

INSERT INTO users (id, full_name, student_id, email, password, role, department_name, created_at) VALUES
-- College of Agriculture
('d1a2b3c4-e5f6-7890-abcd-ef1234567891', 'College of Agriculture', NULL, 'lspu.coa@gmail.com', 'lspudept123', 'department', 'College of Agriculture', NOW()),

-- College of Arts and Sciences
('d2a2b3c4-e5f6-7890-abcd-ef1234567892', 'College of Arts and Sciences', NULL, 'lspu.cas@gmail.com', 'lspudept123', 'department', 'College of Arts and Sciences', NOW()),

-- College of Business Administration and Accountancy
('d3a2b3c4-e5f6-7890-abcd-ef1234567893', 'College of Business Administration and Accountancy', NULL, 'lspu.cbaa@gmail.com', 'lspudept123', 'department', 'College of Business Administration and Accountancy', NOW()),

-- College of Criminal Justice Education
('d4a2b3c4-e5f6-7890-abcd-ef1234567894', 'College of Criminal Justice Education', NULL, 'lspu.ccje@gmail.com', 'lspudept123', 'department', 'College of Criminal Justice Education', NOW()),

-- College of Computer Studies (already exists, this is just for reference)
-- ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'College of Computer Studies', NULL, 'lspu.ccs01@gmail.com', 'lspuccs123', 'department', 'College of Computer Studies', '2025-01-15 10:00:00'),

-- College of Food Nutrition and Dietetics
('d5a2b3c4-e5f6-7890-abcd-ef1234567895', 'College of Food Nutrition and Dietetics', NULL, 'lspu.cfnd@gmail.com', 'lspudept123', 'department', 'College of Food Nutrition and Dietetics', NOW()),

-- College of International Hospitality and Tourism Management
('d6a2b3c4-e5f6-7890-abcd-ef1234567896', 'College of International Hospitality and Tourism Management', NULL, 'lspu.cihtm@gmail.com', 'lspudept123', 'department', 'College of International Hospitality and Tourism Management', NOW()),

-- College of Industrial Technology
('d7a2b3c4-e5f6-7890-abcd-ef1234567897', 'College of Industrial Technology', NULL, 'lspu.cit@gmail.com', 'lspudept123', 'department', 'College of Industrial Technology', NOW()),

-- College of Engineering
('d8a2b3c4-e5f6-7890-abcd-ef1234567898', 'College of Engineering', NULL, 'lspu.coe@gmail.com', 'lspudept123', 'department', 'College of Engineering', NOW()),

-- College of Teacher Education
('d9a2b3c4-e5f6-7890-abcd-ef1234567899', 'College of Teacher Education', NULL, 'lspu.cte@gmail.com', 'lspudept123', 'department', 'College of Teacher Education', NOW())

ON CONFLICT (id) DO NOTHING;

-- Summary
-- Total: 10 Department Accounts (including existing CCS)
-- Email Pattern: lspu.[abbreviation]@gmail.com
-- Password: lspudept123 (for all new accounts)
-- Role: department
-- 
-- Login Credentials:
-- 1. College of Agriculture - lspu.coa@gmail.com / lspudept123
-- 2. College of Arts and Sciences - lspu.cas@gmail.com / lspudept123
-- 3. College of Business Administration and Accountancy - lspu.cbaa@gmail.com / lspudept123
-- 4. College of Criminal Justice Education - lspu.ccje@gmail.com / lspudept123
-- 5. College of Computer Studies - lspu.ccs01@gmail.com / lspuccs123 (existing)
-- 6. College of Food Nutrition and Dietetics - lspu.cfnd@gmail.com / lspudept123
-- 7. College of International Hospitality and Tourism Management - lspu.cihtm@gmail.com / lspudept123
-- 8. College of Industrial Technology - lspu.cit@gmail.com / lspudept123
-- 9. College of Engineering - lspu.coe@gmail.com / lspudept123
-- 10. College of Teacher Education - lspu.cte@gmail.com / lspudept123
