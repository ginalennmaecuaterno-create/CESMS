# Conflict Detection Testing Guide

## What the System Prevents

The conflict detection system prevents:
1. **Time conflicts** - Two events at the same location and overlapping time
2. **Location conflicts** - Two events at the same place and date with overlapping schedules
3. **Checks against approved events** - Active events only (excludes Completed/Cancelled)
4. **Checks against pending requests** - Prevents multiple departments from requesting the same slot

---

## Test Scenarios

### Scenario 1: Department Request vs Approved Event
**Goal:** Verify that department cannot request a time slot that conflicts with an approved event

**Steps:**
1. Login as OSAS
2. Create an event:
   - Event Name: "OSAS Foundation Day"
   - Location: "Main Auditorium"
   - Date: December 20, 2025
   - Start Time: 09:00 AM
   - End Time: 12:00 PM
3. Logout and login as Department
4. Try to request an event with conflicting time:
   - Event Name: "Department Seminar"
   - Location: "Main Auditorium" (same)
   - Date: December 20, 2025 (same)
   - Start Time: 10:00 AM (overlaps!)
   - End Time: 01:00 PM
5. Click "Submit Request"

**Expected Result:**
❌ Form submission should be BLOCKED with error message:
"Schedule conflict detected! This time slot conflicts with: Approved Event 'OSAS Foundation Day' (09:00 AM - 12:00 PM)"

---

### Scenario 2: Department Request vs Another Pending Request
**Goal:** Verify that departments cannot request the same time slot

**Steps:**
1. Login as Department A
2. Request an event:
   - Event Name: "CS Department Workshop"
   - Location: "Computer Lab"
   - Date: December 21, 2025
   - Start Time: 02:00 PM
   - End Time: 05:00 PM
3. Submit (should succeed)
4. Logout and login as Department B
5. Try to request conflicting event:
   - Event Name: "IT Department Training"
   - Location: "Computer Lab" (same)
   - Date: December 21, 2025 (same)
   - Start Time: 03:00 PM (overlaps!)
   - End Time: 06:00 PM
6. Click "Submit Request"

**Expected Result:**
❌ Form submission should be BLOCKED with error message:
"Schedule conflict detected! This time slot conflicts with: Pending Request 'CS Department Workshop' (02:00 PM - 05:00 PM)"

---

### Scenario 3: OSAS Create Event vs Pending Request
**Goal:** Verify that OSAS cannot create event that conflicts with pending requests

**Steps:**
1. Login as Department
2. Request an event:
   - Event Name: "Department Meeting"
   - Location: "Conference Room"
   - Date: December 22, 2025
   - Start Time: 10:00 AM
   - End Time: 12:00 PM
3. Submit (should succeed - status: Pending)
4. Logout and login as OSAS
5. Try to create event with conflict:
   - Event Name: "OSAS Staff Meeting"
   - Location: "Conference Room" (same)
   - Date: December 22, 2025 (same)
   - Start Time: 11:00 AM (overlaps!)
   - End Time: 01:00 PM
6. Click "Create Event"

**Expected Result:**
❌ Form submission should be BLOCKED with error message:
"Schedule conflict detected! This time slot conflicts with: Pending Request 'Department Meeting' (10:00 AM - 12:00 PM)"

---

### Scenario 4: No Conflict - Different Location
**Goal:** Verify that same time but different location is allowed

**Steps:**
1. Login as OSAS
2. Create event:
   - Event Name: "Event A"
   - Location: "Gymnasium"
   - Date: December 23, 2025
   - Start Time: 09:00 AM
   - End Time: 12:00 PM
3. Submit (should succeed)
4. Create another event:
   - Event Name: "Event B"
   - Location: "Auditorium" (different!)
   - Date: December 23, 2025 (same date)
   - Start Time: 09:00 AM (same time)
   - End Time: 12:00 PM
5. Click "Create Event"

**Expected Result:**
✅ Form submission should SUCCEED - no conflict because different location

---

### Scenario 5: No Conflict - Different Date
**Goal:** Verify that same location and time but different date is allowed

**Steps:**
1. Login as Department
2. Request event:
   - Event Name: "Workshop Day 1"
   - Location: "Room 101"
   - Date: December 24, 2025
   - Start Time: 02:00 PM
   - End Time: 05:00 PM
3. Submit (should succeed)
4. Request another event:
   - Event Name: "Workshop Day 2"
   - Location: "Room 101" (same)
   - Date: December 25, 2025 (different!)
   - Start Time: 02:00 PM (same time)
   - End Time: 05:00 PM
5. Click "Submit Request"

**Expected Result:**
✅ Form submission should SUCCEED - no conflict because different date

---

### Scenario 6: No Conflict - Non-Overlapping Time
**Goal:** Verify that same location and date but non-overlapping time is allowed

**Steps:**
1. Login as OSAS
2. Create event:
   - Event Name: "Morning Session"
   - Location: "Main Hall"
   - Date: December 26, 2025
   - Start Time: 08:00 AM
   - End Time: 10:00 AM
3. Submit (should succeed)
4. Create another event:
   - Event Name: "Afternoon Session"
   - Location: "Main Hall" (same)
   - Date: December 26, 2025 (same)
   - Start Time: 10:00 AM (starts when first ends)
   - End Time: 12:00 PM
5. Click "Create Event"

**Expected Result:**
✅ Form submission should SUCCEED - no overlap (10:00 AM is not < 10:00 AM)

---

### Scenario 7: Conflict Detection in OSAS Request Management
**Goal:** Verify visual conflict indicators in request management page

**Steps:**
1. Login as Department A
2. Request event:
   - Event Name: "Request A"
   - Location: "Lab 1"
   - Date: December 27, 2025
   - Start Time: 01:00 PM
   - End Time: 03:00 PM
3. Submit
4. Login as Department B
5. Request conflicting event:
   - Event Name: "Request B"
   - Location: "Lab 1" (same)
   - Date: December 27, 2025 (same)
   - Start Time: 02:00 PM (overlaps!)
   - End Time: 04:00 PM
6. Submit
7. Login as OSAS
8. Go to "Event Request Management"

**Expected Result:**
- Both requests should show with "Conflict" badge (red border)
- Conflict details should show what they conflict with
- Trying to approve either one should show error message

---

### Scenario 8: Completed/Cancelled Events Don't Block
**Goal:** Verify that completed or cancelled events don't cause conflicts

**Steps:**
1. Login as OSAS
2. Create and complete an event (or cancel it):
   - Event Name: "Old Event"
   - Location: "Sports Complex"
   - Date: December 28, 2025
   - Start Time: 09:00 AM
   - End Time: 11:00 AM
   - Status: Completed or Cancelled
3. Try to create new event with same details:
   - Event Name: "New Event"
   - Location: "Sports Complex" (same)
   - Date: December 28, 2025 (same)
   - Start Time: 09:00 AM (same)
   - End Time: 11:00 AM
4. Click "Create Event"

**Expected Result:**
✅ Form submission should SUCCEED - completed/cancelled events don't block

---

## Quick Test Checklist

- [ ] Department request blocked by approved event
- [ ] Department request blocked by another pending request
- [ ] OSAS create event blocked by pending request
- [ ] Different location = no conflict
- [ ] Different date = no conflict
- [ ] Non-overlapping time = no conflict
- [ ] Visual conflict indicators in OSAS request management
- [ ] Completed/Cancelled events don't cause conflicts
- [ ] Error messages show specific conflict details

---

## How to Verify It's Working

1. **Error Message Format:**
   - Should say "Schedule conflict detected!"
   - Should list what it conflicts with
   - Should show the conflicting event/request name
   - Should show the time range

2. **Visual Indicators (OSAS Request Management):**
   - Red border on conflicting request cards
   - "Conflict" badge with warning icon
   - Conflict details showing what it conflicts with

3. **Approval Blocking:**
   - Cannot approve a request that has conflicts
   - Error message explains the conflict

---

## Notes

- The system checks conflicts at **form submission time** (earliest prevention)
- Also checks at **approval time** (double safety)
- Shows **visual indicators** in request management (easy identification)
- Only checks **Active** events (not Completed/Cancelled)
- Checks both **approved events** and **pending requests**
