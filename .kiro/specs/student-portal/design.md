# Design Document - Student Portal

## Overview

The Student Portal is a Flask-based web application module that provides students with access to campus events and registration management. The system integrates with the existing CESMS architecture, utilizing Supabase for data persistence and authentication. The portal implements role-based access control to ensure students can only access their own data and appropriate event information.

The design follows the existing MVC pattern used in the CESMS application, with controllers handling business logic, models managing data access, and Jinja2 templates rendering the user interface. The system distinguishes between two event types: limited-seat events requiring department approval and free-for-all events with automatic approval.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Student Portal Layer                     │
├─────────────────────────────────────────────────────────────┤
│  Routes (Blueprint)                                          │
│  ├─ /student/dashboard                                       │
│  ├─ /student/events                                          │
│  ├─ /student/registrations                                   │
│  └─ /student/ticket/<registration_id>                        │
├─────────────────────────────────────────────────────────────┤
│  Controllers                                                 │
│  ├─ student_dashboard_controller.py                          │
│  ├─ student_events_controller.py                             │
│  └─ student_registrations_controller.py                      │
├─────────────────────────────────────────────────────────────┤
│  Models                                                      │
│  ├─ student_events.py (read events)                          │
│  └─ student_registrations.py (CRUD registrations)            │
├─────────────────────────────────────────────────────────────┤
│  Templates                                                   │
│  ├─ base_student.html                                        │
│  ├─ student_dashboard.html                                   │
│  ├─ student_events.html                                      │
│  ├─ student_registrations.html                               │
│  └─ student_ticket.html                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Shared Infrastructure                      │
├─────────────────────────────────────────────────────────────┤
│  Authentication (Supabase Auth)                              │
│  Session Management (Flask Session)                          │
│  Database (Supabase PostgreSQL)                              │
│  QR Code Generation (qrcode library)                         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Event Browsing Flow**
   - Student requests events page → Controller fetches active events from database → Template renders event list with registration status

2. **Registration Flow (Limited-Seat)**
   - Student clicks register → Controller validates (no duplicate, seats available) → Creates pending registration → Department reviews → Upon approval, QR code generated → Student accesses ticket

3. **Registration Flow (Free-For-All)**
   - Student clicks register → Controller validates (no duplicate) → Creates approved registration (no QR code) → Confirmation displayed

4. **Ticket Access Flow**
   - Student views approved registration → Controller retrieves registration with QR code → Template displays ticket with QR code image

## Components and Interfaces

### 1. Routes (Blueprint)

**File:** `routes/student_routes.py`

```python
from flask import Blueprint

student_bp = Blueprint('student', __name__, url_prefix='/student')

# Route definitions
@student_bp.route('/dashboard')
@student_bp.route('/events')
@student_bp.route('/events/register/<event_id>', methods=['POST'])
@student_bp.route('/registrations')
@student_bp.route('/registrations/cancel/<registration_id>', methods=['POST'])
@student_bp.route('/ticket/<registration_id>')
```

### 2. Controllers

#### StudentDashboardController
**File:** `controllers/student_dashboard_controller.py`

**Responsibilities:**
- Verify student authentication
- Fetch registration statistics
- Render dashboard view

**Key Methods:**
- `view_dashboard()`: Main dashboard handler

#### StudentEventsController
**File:** `controllers/student_events_controller.py`

**Responsibilities:**
- Display active events
- Handle event registration
- Check registration eligibility
- Differentiate between limited and free-for-all events

**Key Methods:**
- `view_events()`: Display all active events
- `register_for_event(event_id)`: Create registration

#### StudentRegistrationsController
**File:** `controllers/student_registrations_controller.py`

**Responsibilities:**
- Display student's registrations
- Handle registration cancellation
- Display QR code tickets

**Key Methods:**
- `view_registrations()`: List all registrations
- `cancel_registration(registration_id)`: Cancel pending registration
- `view_ticket(registration_id)`: Display QR code ticket

### 3. Models

#### StudentEvents Model
**File:** `models/student_events.py`

**Responsibilities:**
- Fetch active events
- Get event details
- Check seat availability
- Determine event type

**Key Methods:**
```python
@staticmethod
def get_active_events() -> Response
    """Fetch all active events with department info"""

@staticmethod
def get_event_by_id(event_id: str) -> Response
    """Get specific event details"""

@staticmethod
def get_available_seats(event_id: str) -> int
    """Calculate remaining seats for limited events"""

@staticmethod
def is_free_for_all(event_id: str) -> bool
    """Check if event is free-for-all (no participant limit)"""
```

#### StudentRegistrations Model
**File:** `models/student_registrations.py`

**Responsibilities:**
- Create registrations
- Fetch student's registrations
- Cancel registrations
- Check for duplicate registrations
- Retrieve QR code data

**Key Methods:**
```python
@staticmethod
def create_registration(student_id: str, event_id: str, auto_approve: bool) -> Response
    """Create new registration (pending or approved based on event type)"""

@staticmethod
def get_student_registrations(student_id: str) -> Response
    """Fetch all registrations for a student"""

@staticmethod
def has_registered(student_id: str, event_id: str) -> bool
    """Check if student already registered for event"""

@staticmethod
def cancel_registration(registration_id: str, student_id: str) -> bool
    """Cancel a pending registration"""

@staticmethod
def get_registration_with_qr(registration_id: str, student_id: str) -> Response
    """Get registration details including QR code"""

@staticmethod
def get_registration_counts(student_id: str) -> dict
    """Get count of registrations by status"""
```

## Data Models

### Database Schema

#### Events Table (existing)
```
events
├─ id (uuid, PK)
├─ department_id (uuid, FK → users.id)
├─ event_name (text)
├─ description (text)
├─ location (text)
├─ date (date)
├─ start_time (time)
├─ end_time (time)
├─ participant_limit (integer, nullable) ← NULL means free-for-all
├─ status (text) ← 'Active', 'Completed', 'Cancelled'
└─ created_at (timestamp)
```

#### Registrations Table (existing)
```
registrations
├─ id (uuid, PK)
├─ student_id (uuid, FK → users.id)
├─ event_id (uuid, FK → events.id)
├─ registration_status (text) ← 'Pending', 'Approved', 'Rejected'
├─ unique_code (text, nullable) ← QR code data (only for approved limited-seat)
└─ created_at (timestamp)
```

#### Users Table (existing)
```
users
├─ id (uuid, PK)
├─ full_name (text)
├─ student_id (text)
├─ email (text)
├─ role (text) ← 'student', 'department', 'osas'
└─ department_name (text, nullable)
```

### Key Relationships

- A student (user with role='student') can have many registrations
- An event can have many registrations
- A registration belongs to one student and one event
- Limited-seat events have participant_limit > 0
- Free-for-all events have participant_limit = NULL

### Event Type Determination

```python
def is_limited_seat_event(event):
    return event['participant_limit'] is not None and event['participant_limit'] > 0

def is_free_for_all_event(event):
    return event['participant_limit'] is None
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Dashboard displays correct user information
*For any* authenticated student user, the dashboard should display their full name and email exactly as stored in the database.
**Validates: Requirements 1.2**

### Property 2: Dashboard registration counts are accurate
*For any* student, the pending registration count displayed should equal the number of registrations with status "Pending", and the approved count should equal the number with status "Approved".
**Validates: Requirements 1.3, 1.4**

### Property 3: Only active events are displayed in browsing
*For any* events list displayed to students, all events should have status "Active" and no events with status "Cancelled" or "Completed" should appear.
**Validates: Requirements 2.1, 8.1, 8.4**

### Property 4: Event display includes all required information
*For any* event displayed in the events list, the rendered output should contain the event name, description, date, time, location, and organizer name.
**Validates: Requirements 2.2**

### Property 5: Event type classification is correct
*For any* event, it should be classified as limited-seat if and only if participant_limit is not null and greater than zero, otherwise it should be classified as free-for-all.
**Validates: Requirements 2.3**

### Property 6: Remaining seats calculation is accurate
*For any* limited-seat event, the displayed remaining seats should equal participant_limit minus the count of approved registrations for that event.
**Validates: Requirements 2.4**

### Property 7: Events are sorted chronologically
*For any* list of events displayed, each event's date should be less than or equal to the next event's date in the list.
**Validates: Requirements 2.5**

### Property 8: Registration status indication is correct
*For any* student viewing an event, if a registration exists for that student and event, it should be indicated; if no registration exists, no indication should appear.
**Validates: Requirements 2.6**

### Property 9: Limited-seat registrations start as pending
*For any* registration created for a limited-seat event, the registration_status should be "Pending".
**Validates: Requirements 3.1**

### Property 10: Duplicate registrations are prevented
*For any* student and event, attempting to create a second registration when one already exists should fail, regardless of event type.
**Validates: Requirements 3.2, 4.2**

### Property 11: Full events reject new registrations
*For any* limited-seat event where the count of approved registrations equals participant_limit, attempting to create a new registration should fail.
**Validates: Requirements 3.3**

### Property 12: Registration data persistence
*For any* registration created, querying the database should return a record containing the student_id, event_id, and a created_at timestamp.
**Validates: Requirements 3.5, 4.5**

### Property 13: Free-for-all registrations are auto-approved
*For any* registration created for a free-for-all event, the registration_status should be "Approved".
**Validates: Requirements 4.1**

### Property 14: Free-for-all registrations have no QR code
*For any* registration for a free-for-all event, the unique_code field should be null.
**Validates: Requirements 4.3**

### Property 15: All student registrations are displayed
*For any* student viewing their registrations page, the count of displayed registrations should equal the count of registrations in the database for that student.
**Validates: Requirements 5.1**

### Property 16: Registration display includes required information
*For any* registration displayed, the rendered output should contain the event name, date, time, location, and registration status.
**Validates: Requirements 5.2**

### Property 17: Registration filtering works correctly
*For any* status filter applied (Pending, Approved, Rejected), all displayed registrations should have that status, and no registrations with other statuses should appear.
**Validates: Requirements 5.3**

### Property 18: Registrations are sorted by event date
*For any* list of registrations displayed, each registration's event date should be less than or equal to the next registration's event date.
**Validates: Requirements 5.4**

### Property 19: Pending registrations can be cancelled
*For any* registration with status "Pending", the cancel action should be available and successfully remove the registration from the database.
**Validates: Requirements 5.5, 7.1**

### Property 20: Approved limited-seat registrations have QR codes
*For any* registration with status "Approved" for a limited-seat event, the unique_code field should contain a non-null value.
**Validates: Requirements 6.1**

### Property 21: QR code tickets display event information
*For any* approved limited-seat registration, the ticket page should display the event name, date, time, and location.
**Validates: Requirements 6.2, 6.3**

### Property 22: QR codes uniquely identify registrations
*For any* unique_code value, querying the database should return exactly one registration.
**Validates: Requirements 6.5**

### Property 23: Non-pending registrations cannot be cancelled
*For any* registration with status "Approved" or "Rejected", attempting to cancel should fail and the registration should remain in the database.
**Validates: Requirements 7.2, 7.3**

### Property 24: Cancellation updates seat availability
*For any* limited-seat event, after cancelling a registration, the available seats should increase by one.
**Validates: Requirements 7.5**

### Property 25: Cancelled events are indicated in registrations
*For any* registration where the associated event has status "Cancelled", the registration view should display a cancellation notice.
**Validates: Requirements 8.2, 8.3**

### Property 26: All registrations shown regardless of event status
*For any* student viewing their registrations, registrations for events with any status (Active, Cancelled, Completed) should all be displayed.
**Validates: Requirements 8.5**

### Property 27: Role-based access control is enforced
*For any* user with role "department" or "osas", attempting to access student portal pages should result in access denial.
**Validates: Requirements 9.2, 9.3**

### Property 28: Navigation is consistent across pages
*For any* student portal page, the rendered output should contain the navigation menu with links to dashboard, events, and registrations.
**Validates: Requirements 10.1**

### Property 29: Errors produce user-friendly messages
*For any* error condition (validation failure, database error, etc.), the response should include a user-friendly error message.
**Validates: Requirements 10.4**

## Error Handling

### Validation Errors

1. **Duplicate Registration**: When a student attempts to register for an event they're already registered for, return HTTP 400 with message "You have already registered for this event."

2. **Event Full**: When a student attempts to register for a full limited-seat event, return HTTP 400 with message "This event is full. No more seats available."

3. **Event Not Active**: When a student attempts to register for a non-active event, return HTTP 400 with message "This event is no longer accepting registrations."

4. **Invalid Cancellation**: When a student attempts to cancel a non-pending registration, return HTTP 400 with message "Only pending registrations can be cancelled."

### Authorization Errors

1. **Unauthenticated Access**: When an unauthenticated user attempts to access student pages, redirect to login with flash message "Please login first."

2. **Wrong Role**: When a user with role other than "student" attempts to access student pages, return HTTP 403 with message "Access denied. Student accounts only."

3. **Wrong Student**: When a student attempts to access another student's registration or ticket, return HTTP 403 with message "Access denied."

### Database Errors

1. **Connection Failure**: When database connection fails, return HTTP 500 with message "Service temporarily unavailable. Please try again later."

2. **Query Failure**: When a database query fails, log the error and return HTTP 500 with message "An error occurred. Please try again."

### Not Found Errors

1. **Event Not Found**: When accessing a non-existent event, return HTTP 404 with message "Event not found."

2. **Registration Not Found**: When accessing a non-existent registration, return HTTP 404 with message "Registration not found."

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **Authentication Tests**
   - Test unauthenticated access redirects to login
   - Test wrong role access is denied
   - Test student role access is granted

2. **Event Display Tests**
   - Test empty events list displays correctly
   - Test single event displays all required fields
   - Test events with null participant_limit are classified as free-for-all

3. **Registration Creation Tests**
   - Test first registration for an event succeeds
   - Test registration for event with one seat remaining succeeds
   - Test registration for full event fails

4. **Cancellation Tests**
   - Test cancelling pending registration succeeds
   - Test cancelling approved registration fails
   - Test cancelling non-existent registration fails

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using the **Hypothesis** library for Python. Each test will run a minimum of 100 iterations with randomly generated data.

1. **Property Tests for Event Display**
   - Generate random sets of events with various statuses
   - Verify only active events appear in browsing
   - Verify all events are sorted by date
   - Verify event type classification matches participant_limit

2. **Property Tests for Registration Logic**
   - Generate random students and events
   - Verify duplicate prevention works for all combinations
   - Verify seat counting is accurate for all limited-seat events
   - Verify auto-approval works for all free-for-all events

3. **Property Tests for Data Integrity**
   - Generate random registrations
   - Verify all registrations have required fields
   - Verify QR codes are unique across all registrations
   - Verify cancellation updates seat counts correctly

4. **Property Tests for Filtering and Sorting**
   - Generate random registration sets with various statuses
   - Verify filtering returns only matching statuses
   - Verify sorting maintains chronological order
   - Verify counts match actual database records

Each property-based test will be tagged with a comment referencing the correctness property it implements using the format: `# Feature: student-portal, Property X: [property text]`

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Complete Registration Flow**
   - Student logs in → views events → registers → views registration → sees pending status

2. **Approval and Ticket Flow**
   - Department approves registration → student views registration → QR code is displayed

3. **Cancellation Flow**
   - Student registers → cancels → registration removed → seat count updated

4. **Event Status Changes**
   - Event is cancelled → student views registrations → cancellation notice appears

## Implementation Notes

### QR Code Generation

QR codes will be generated using the `qrcode` library when a registration is approved by the department. The unique_code will be a UUID stored in the database, and the QR code image will be generated on-demand when viewing the ticket.

```python
import qrcode
import uuid

def generate_qr_code(registration_id):
    unique_code = str(uuid.uuid4())
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(unique_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return unique_code, img
```

### Session Management

Student authentication will use Flask sessions with the following data:
- `user_email`: Student's email address
- `user_name`: Student's full name
- `user_role`: Should be "student"
- `user_id`: Student's database ID

### Performance Considerations

1. **Event Queries**: Index on `status` column for fast filtering of active events
2. **Registration Queries**: Composite index on `(student_id, event_id)` for duplicate checking
3. **Seat Counting**: Consider caching seat counts for popular events
4. **QR Code Generation**: Generate QR codes asynchronously when possible

### Security Considerations

1. **SQL Injection**: Use parameterized queries (Supabase handles this)
2. **XSS Prevention**: Escape all user input in templates (Jinja2 auto-escapes)
3. **CSRF Protection**: Use Flask-WTF for form protection
4. **Session Security**: Use secure, httponly cookies
5. **Authorization**: Always verify student_id matches session user_id before data access
