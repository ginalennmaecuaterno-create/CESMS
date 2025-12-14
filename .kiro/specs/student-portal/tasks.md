# Implementation Plan - Student Portal

- [ ] 1. Set up student portal infrastructure
  - [x] 1.1 Create student routes blueprint



    - Create `routes/student_routes.py` with blueprint definition
    - Define route endpoints for dashboard, events, registrations, and tickets
    - Register blueprint in `app.py`


    - _Requirements: 1.1, 9.1_

  - [ ] 1.2 Create base student template
    - Create `templates/base_student.html` with navigation menu
    - Include links to dashboard, events, and registrations



    - Add logout functionality
    - Style with consistent LSPU branding
    - _Requirements: 1.5, 10.1_



  - [ ] 1.3 Create student CSS file
    - Create `static/css/student.css` for student portal styling
    - Implement responsive design for mobile devices
    - Ensure consistent visual hierarchy
    - _Requirements: 10.2, 10.5_

- [ ] 2. Implement student data models
  - [ ] 2.1 Create StudentEvents model
    - Create `models/student_events.py`
    - Implement `get_active_events()` method
    - Implement `get_event_by_id(event_id)` method
    - Implement `get_available_seats(event_id)` method
    - Implement `is_free_for_all(event_id)` method
    - _Requirements: 2.1, 2.3, 2.4_

  - [ ] 2.2 Write property test for active events filtering
    - **Property 3: Only active events are displayed in browsing**
    - **Validates: Requirements 2.1, 8.1, 8.4**




  - [ ] 2.3 Write property test for event type classification
    - **Property 5: Event type classification is correct**
    - **Validates: Requirements 2.3**

  - [ ] 2.4 Write property test for seat calculation
    - **Property 6: Remaining seats calculation is accurate**
    - **Validates: Requirements 2.4**

  - [ ] 2.5 Create StudentRegistrations model
    - Create `models/student_registrations.py`
    - Implement `create_registration(student_id, event_id, auto_approve)` method
    - Implement `get_student_registrations(student_id)` method
    - Implement `has_registered(student_id, event_id)` method
    - Implement `cancel_registration(registration_id, student_id)` method
    - Implement `get_registration_with_qr(registration_id, student_id)` method


    - Implement `get_registration_counts(student_id)` method
    - _Requirements: 3.1, 3.2, 4.1, 5.1, 7.1_

  - [ ] 2.6 Write property test for duplicate prevention
    - **Property 10: Duplicate registrations are prevented**
    - **Validates: Requirements 3.2, 4.2**




  - [ ] 2.7 Write property test for registration data persistence
    - **Property 12: Registration data persistence**
    - **Validates: Requirements 3.5, 4.5**

- [ ] 3. Implement student dashboard
  - [ ] 3.1 Create dashboard controller
    - Create `controllers/student_dashboard_controller.py`
    - Implement `view_dashboard()` function
    - Add authentication check (redirect if not logged in)
    - Add role check (deny access if not student)
    - Fetch registration counts using `get_registration_counts()`
    - _Requirements: 1.1, 1.3, 1.4, 9.1, 9.2, 9.3_

  - [ ] 3.2 Create dashboard template
    - Create `templates/student_dashboard.html`
    - Display student name and email
    - Show pending registrations count
    - Show approved registrations count
    - Add quick links to events and registrations
    - _Requirements: 1.2, 1.3, 1.4, 1.5_

  - [ ] 3.3 Write property test for dashboard user information
    - **Property 1: Dashboard displays correct user information**


    - **Validates: Requirements 1.2**

  - [ ] 3.4 Write property test for registration counts
    - **Property 2: Dashboard registration counts are accurate**
    - **Validates: Requirements 1.3, 1.4**

  - [ ] 3.5 Write unit tests for dashboard authentication
    - Test unauthenticated access redirects to login



    - Test department role access is denied
    - Test OSAS role access is denied
    - Test student role access is granted
    - _Requirements: 9.1, 9.2, 9.3_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement event browsing
  - [ ] 5.1 Create events controller
    - Create `controllers/student_events_controller.py`
    - Implement `view_events()` function
    - Add authentication and role checks
    - Fetch active events using `get_active_events()`
    - For each event, check if student has registered using `has_registered()`
    - Calculate available seats for limited-seat events
    - Sort events by date
    - _Requirements: 2.1, 2.4, 2.5, 2.6_

  - [x] 5.2 Create events template

    - Create `templates/student_events.html`
    - Display event cards with all required information (name, description, date, time, location, organizer)
    - Show event type indicator (limited-seat vs free-for-all)
    - Show remaining seats for limited-seat events
    - Show "Already Registered" badge if applicable
    - Add register button for events not yet registered
    - Disable register button for full events
    - _Requirements: 2.2, 2.3, 2.4, 2.6_

  - [ ] 5.3 Write property test for event display information
    - **Property 4: Event display includes all required information**
    - **Validates: Requirements 2.2**

  - [ ] 5.4 Write property test for event sorting
    - **Property 7: Events are sorted chronologically**
    - **Validates: Requirements 2.5**

  - [ ] 5.5 Write property test for registration status indication
    - **Property 8: Registration status indication is correct**
    - **Validates: Requirements 2.6**

- [ ] 6. Implement event registration
  - [ ] 6.1 Add registration handler to events controller
    - Implement `register_for_event(event_id)` function in `student_events_controller.py`
    - Add authentication and role checks
    - Validate event exists and is active
    - Check for duplicate registration using `has_registered()`
    - For limited-seat events: check seats available, create pending registration
    - For free-for-all events: create approved registration
    - Display success or error message
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.4_

  - [ ] 6.2 Write property test for limited-seat registration status
    - **Property 9: Limited-seat registrations start as pending**
    - **Validates: Requirements 3.1**

  - [x] 6.3 Write property test for full event rejection


    - **Property 11: Full events reject new registrations**
    - **Validates: Requirements 3.3**

  - [ ] 6.4 Write property test for free-for-all auto-approval
    - **Property 13: Free-for-all registrations are auto-approved**
    - **Validates: Requirements 4.1**



  - [ ] 6.5 Write property test for free-for-all QR code absence
    - **Property 14: Free-for-all registrations have no QR code**
    - **Validates: Requirements 4.3**

  - [ ] 6.6 Write unit tests for registration validation
    - Test registration for non-existent event fails
    - Test registration for cancelled event fails
    - Test registration for completed event fails
    - Test duplicate registration fails
    - Test registration for full event fails
    - _Requirements: 3.2, 3.3_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement registration management
  - [ ] 8.1 Create registrations controller
    - Create `controllers/student_registrations_controller.py`
    - Implement `view_registrations()` function
    - Add authentication and role checks
    - Fetch student registrations using `get_student_registrations()`
    - Support status filtering (All, Pending, Approved, Rejected)
    - Sort registrations by event date
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 8.2 Create registrations template
    - Create `templates/student_registrations.html`
    - Display registration cards with event details and status
    - Add status filter buttons (All, Pending, Approved, Rejected)
    - Show cancel button for pending registrations
    - Show "View Ticket" button for approved limited-seat registrations
    - Show cancellation notice for cancelled events

    - _Requirements: 5.2, 5.5, 8.2_

  - [ ] 8.3 Write property test for registration display completeness
    - **Property 15: All student registrations are displayed**
    - **Validates: Requirements 5.1**

  - [ ] 8.4 Write property test for registration information display
    - **Property 16: Registration display includes required information**
    - **Validates: Requirements 5.2**

  - [ ] 8.5 Write property test for registration filtering
    - **Property 17: Registration filtering works correctly**
    - **Validates: Requirements 5.3**

  - [ ] 8.6 Write property test for registration sorting
    - **Property 18: Registrations are sorted by event date**
    - **Validates: Requirements 5.4**

  - [ ] 8.7 Write property test for cancelled event indication
    - **Property 25: Cancelled events are indicated in registrations**
    - **Validates: Requirements 8.2, 8.3**

  - [ ] 8.8 Write property test for showing all registrations
    - **Property 26: All registrations shown regardless of event status**
    - **Validates: Requirements 8.5**

- [ ] 9. Implement registration cancellation
  - [ ] 9.1 Add cancellation handler to registrations controller
    - Implement `cancel_registration(registration_id)` function in `student_registrations_controller.py`

    - Add authentication and role checks
    - Verify registration belongs to current student
    - Verify registration status is "Pending"
    - Call `cancel_registration()` model method
    - Display success or error message
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 9.2 Write property test for pending cancellation
    - **Property 19: Pending registrations can be cancelled**



    - **Validates: Requirements 5.5, 7.1**

  - [ ] 9.3 Write property test for non-pending cancellation prevention
    - **Property 23: Non-pending registrations cannot be cancelled**
    - **Validates: Requirements 7.2, 7.3**

  - [ ] 9.4 Write property test for seat availability update
    - **Property 24: Cancellation updates seat availability**
    - **Validates: Requirements 7.5**

  - [ ] 9.5 Write unit tests for cancellation authorization
    - Test cancelling another student's registration fails
    - Test cancelling non-existent registration fails
    - _Requirements: 7.1_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement QR code ticket display
  - [ ] 11.1 Add ticket view handler to registrations controller
    - Implement `view_ticket(registration_id)` function in `student_registrations_controller.py`
    - Add authentication and role checks
    - Verify registration belongs to current student
    - Verify registration is approved
    - Verify event is limited-seat (has participant_limit)
    - Fetch registration with QR code using `get_registration_with_qr()`
    - Generate QR code image from unique_code
    - _Requirements: 6.1, 6.2, 6.5_

  - [ ] 11.2 Create ticket template
    - Create `templates/student_ticket.html`
    - Display QR code image prominently
    - Show event name, date, time, and location
    - Add download button for ticket
    - Style as a printable ticket
    - _Requirements: 6.2, 6.3, 6.4_

  - [ ] 11.3 Write property test for QR code generation
    - **Property 20: Approved limited-seat registrations have QR codes**
    - **Validates: Requirements 6.1**

  - [ ] 11.4 Write property test for QR code display
    - **Property 21: QR code tickets display event information**
    - **Validates: Requirements 6.2, 6.3**

  - [ ] 11.5 Write property test for QR code uniqueness
    - **Property 22: QR codes uniquely identify registrations**
    - **Validates: Requirements 6.5**

  - [ ] 11.6 Write unit tests for ticket access authorization
    - Test viewing another student's ticket fails
    - Test viewing ticket for pending registration fails
    - Test viewing ticket for rejected registration fails
    - Test viewing ticket for free-for-all event fails
    - _Requirements: 6.2_

- [ ] 12. Implement error handling and user feedback
  - [ ] 12.1 Add comprehensive error handling to all controllers
    - Wrap database calls in try-except blocks
    - Return appropriate HTTP status codes (400, 403, 404, 500)
    - Display user-friendly error messages using flash()
    - Log errors for debugging
    - _Requirements: 10.4_

  - [ ] 12.2 Add success feedback messages
    - Add flash messages for successful registration
    - Add flash messages for successful cancellation
    - Add flash messages for successful logout
    - _Requirements: 3.4, 4.4, 7.4_

  - [ ] 12.3 Write property test for error messages
    - **Property 29: Errors produce user-friendly messages**
    - **Validates: Requirements 10.4**

- [ ] 13. Add navigation consistency
  - [ ] 13.1 Update base_student.html navigation
    - Ensure navigation menu appears on all student pages
    - Highlight active page in navigation
    - Add user name display in header
    - Add logout button
    - _Requirements: 10.1_

  - [ ] 13.2 Write property test for navigation consistency
    - **Property 28: Navigation is consistent across pages**
    - **Validates: Requirements 10.1**

- [ ] 14. Implement role-based access control
  - [ ] 14.1 Create authentication decorator
    - Create `utils/auth_decorators.py`
    - Implement `@require_student` decorator
    - Check session for user_email
    - Check user role is "student"
    - Redirect to login if not authenticated
    - Return 403 if wrong role
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ] 14.2 Apply decorator to all student routes
    - Add `@require_student` to all student controller functions
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ] 14.3 Write property test for role-based access control
    - **Property 27: Role-based access control is enforced**
    - **Validates: Requirements 9.2, 9.3**

- [ ] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Create student portal JavaScript
  - [ ] 16.1 Create student.js for interactive features
    - Create `static/js/student.js`
    - Add confirmation dialogs for cancellation
    - Add loading indicators for async actions
    - Add filter toggle functionality for registrations
    - Add responsive menu toggle for mobile
    - _Requirements: 10.3_

  - [ ] 16.2 Add AJAX for registration actions
    - Implement AJAX registration to avoid page reload
    - Implement AJAX cancellation to avoid page reload
    - Update UI dynamically after actions
    - Show loading states during requests
    - _Requirements: 10.3_

- [ ] 17. Polish and refinement
  - [ ] 17.1 Add responsive design improvements
    - Test on mobile devices
    - Adjust layouts for small screens
    - Ensure touch-friendly buttons
    - _Requirements: 10.5_

  - [ ] 17.2 Add accessibility improvements
    - Add ARIA labels to interactive elements
    - Ensure keyboard navigation works
    - Add alt text to images
    - Ensure sufficient color contrast
    - _Requirements: 10.2_

  - [ ] 17.3 Optimize performance
    - Add database indexes for common queries
    - Cache registration counts where appropriate
    - Optimize QR code generation
    - Minimize CSS and JavaScript files
    - _Requirements: Performance considerations from design_

- [ ] 18. Final integration testing
  - [ ] 18.1 Test complete registration workflow
    - Student logs in → views events → registers for limited-seat event → sees pending status → department approves → student views ticket with QR code
    - _Requirements: All_

  - [ ] 18.2 Test complete cancellation workflow
    - Student registers for event → cancels registration → registration removed → seat count updated
    - _Requirements: 7.1, 7.5_

  - [ ] 18.3 Test event status change handling
    - Event is cancelled after registration → student views registrations → cancellation notice appears
    - _Requirements: 8.2_

  - [ ] 18.4 Test free-for-all event workflow
    - Student registers for free-for-all event → registration auto-approved → no QR code generated
    - _Requirements: 4.1, 4.3_
