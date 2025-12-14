# Requirements Document - Student Portal

## Introduction

The Student Portal is a web-based interface that enables LSPU students to discover, register for, and participate in campus events. Students can view upcoming events, submit registration requests, track their registration status, and access QR code tickets for approved event registrations. The system distinguishes between limited-seat events (requiring department approval) and free-for-all events (automatic approval).

## Glossary

- **Student Portal**: The web interface accessible to students with role "student"
- **Event**: A campus activity organized by departments and approved by OSAS
- **Limited-Seat Event**: An event with a participant limit that requires department verification and approval before attendance
- **Free-For-All Event**: An event open to all students with automatic registration approval
- **Registration**: A student's request to attend an event
- **QR Code Ticket**: A unique scannable code provided to students upon registration approval for limited-seat events
- **Event Status**: The current state of an event (Active, Completed, Cancelled)
- **Registration Status**: The current state of a registration (Pending, Approved, Rejected)
- **CESMS**: Campus Event Management System
- **LSPU**: Laguna State Polytechnic University

## Requirements

### Requirement 1: Student Dashboard

**User Story:** As a student, I want to access a dashboard that shows my event activity, so that I can quickly see my registrations and upcoming events.

#### Acceptance Criteria

1. WHEN a student logs in with valid credentials, THE Student Portal SHALL display the student dashboard
2. WHEN the dashboard loads, THE Student Portal SHALL display the student's full name and email
3. WHEN the dashboard loads, THE Student Portal SHALL show a count of the student's pending registrations
4. WHEN the dashboard loads, THE Student Portal SHALL show a count of the student's approved registrations
5. WHEN the dashboard loads, THE Student Portal SHALL provide navigation to view all events and manage registrations

### Requirement 2: Event Discovery and Browsing

**User Story:** As a student, I want to browse all upcoming approved events, so that I can discover activities I'm interested in attending.

#### Acceptance Criteria

1. WHEN a student navigates to the events page, THE Student Portal SHALL display all active events
2. WHEN displaying events, THE Student Portal SHALL show event name, description, date, time, location, and organizer
3. WHEN displaying events, THE Student Portal SHALL indicate whether an event has limited seats or is free-for-all
4. WHEN displaying events, THE Student Portal SHALL show remaining seats for limited-seat events
5. WHEN displaying events, THE Student Portal SHALL sort events by date in ascending order
6. WHEN a student views an event, THE Student Portal SHALL indicate if the student has already registered for that event

### Requirement 3: Event Registration for Limited-Seat Events

**User Story:** As a student, I want to register for limited-seat events, so that I can request approval to attend events that require verification.

#### Acceptance Criteria

1. WHEN a student clicks register on a limited-seat event, THE Student Portal SHALL create a registration with status "Pending"
2. WHEN a student registers for a limited-seat event, THE Student Portal SHALL prevent duplicate registrations for the same event
3. WHEN a limited-seat event is full, THE Student Portal SHALL prevent new registrations
4. WHEN a student registers successfully, THE Student Portal SHALL display a confirmation message
5. WHEN a registration is created, THE Student Portal SHALL store the student ID, event ID, and timestamp

### Requirement 4: Event Registration for Free-For-All Events

**User Story:** As a student, I want to register for free-for-all events with automatic approval, so that I can quickly confirm my attendance without waiting for verification.

#### Acceptance Criteria

1. WHEN a student clicks register on a free-for-all event, THE Student Portal SHALL create a registration with status "Approved"
2. WHEN a student registers for a free-for-all event, THE Student Portal SHALL prevent duplicate registrations for the same event
3. WHEN a student registers for a free-for-all event, THE Student Portal SHALL not generate a QR code
4. WHEN a student registers successfully for a free-for-all event, THE Student Portal SHALL display a confirmation message
5. WHEN a free-for-all registration is created, THE Student Portal SHALL store the student ID, event ID, and timestamp

### Requirement 5: Registration Management

**User Story:** As a student, I want to view all my event registrations and their statuses, so that I can track which events I'm attending and which are pending approval.

#### Acceptance Criteria

1. WHEN a student navigates to the registrations page, THE Student Portal SHALL display all of the student's registrations
2. WHEN displaying registrations, THE Student Portal SHALL show event name, date, time, location, and registration status
3. WHEN displaying registrations, THE Student Portal SHALL allow filtering by status (All, Pending, Approved, Rejected)
4. WHEN displaying registrations, THE Student Portal SHALL sort registrations by event date
5. WHEN a registration is pending, THE Student Portal SHALL allow the student to cancel the registration

### Requirement 6: QR Code Ticket Access

**User Story:** As a student, I want to view and download my QR code ticket for approved limited-seat events, so that I can present it for attendance verification.

#### Acceptance Criteria

1. WHEN a student's registration is approved for a limited-seat event, THE Student Portal SHALL generate a unique QR code
2. WHEN a student views an approved limited-seat registration, THE Student Portal SHALL display the QR code ticket
3. WHEN displaying a QR code, THE Student Portal SHALL show the event name, date, time, and location
4. WHEN displaying a QR code, THE Student Portal SHALL provide a download option for the ticket
5. WHEN a QR code is scanned, THE System SHALL identify the unique registration

### Requirement 7: Registration Cancellation

**User Story:** As a student, I want to cancel my pending registrations, so that I can withdraw from events I can no longer attend.

#### Acceptance Criteria

1. WHEN a student cancels a pending registration, THE Student Portal SHALL remove the registration from the database
2. WHEN a student attempts to cancel an approved registration, THE Student Portal SHALL prevent the cancellation
3. WHEN a student attempts to cancel a rejected registration, THE Student Portal SHALL prevent the cancellation
4. WHEN a registration is cancelled successfully, THE Student Portal SHALL display a confirmation message
5. WHEN a registration is cancelled, THE Student Portal SHALL update the available seats for limited-seat events

### Requirement 8: Event Status Awareness

**User Story:** As a student, I want to see only active events when browsing, so that I don't waste time looking at cancelled or completed events.

#### Acceptance Criteria

1. WHEN displaying the events list, THE Student Portal SHALL show only events with status "Active"
2. WHEN an event is cancelled after a student registers, THE Student Portal SHALL indicate the cancellation in the student's registrations
3. WHEN viewing a cancelled event registration, THE Student Portal SHALL display a cancellation notice
4. WHEN an event is completed, THE Student Portal SHALL remove it from the browsing list
5. WHEN viewing registrations, THE Student Portal SHALL show all registrations regardless of event status

### Requirement 9: User Authentication and Authorization

**User Story:** As a student, I want secure access to my portal, so that only I can view and manage my registrations.

#### Acceptance Criteria

1. WHEN a user accesses student portal pages without logging in, THE Student Portal SHALL redirect to the login page
2. WHEN a user with role "department" attempts to access student pages, THE Student Portal SHALL deny access
3. WHEN a user with role "osas" attempts to access student pages, THE Student Portal SHALL deny access
4. WHEN a student logs out, THE Student Portal SHALL clear the session and redirect to login
5. WHEN a student's session expires, THE Student Portal SHALL require re-authentication

### Requirement 10: Responsive User Interface

**User Story:** As a student, I want a clean and intuitive interface, so that I can easily navigate and use the portal on any device.

#### Acceptance Criteria

1. WHEN the student portal loads, THE Student Portal SHALL display a consistent navigation menu
2. WHEN displaying information, THE Student Portal SHALL use clear visual hierarchy and readable typography
3. WHEN a student performs an action, THE Student Portal SHALL provide immediate visual feedback
4. WHEN errors occur, THE Student Portal SHALL display user-friendly error messages
5. WHEN the portal is accessed on mobile devices, THE Student Portal SHALL adapt the layout for smaller screens
