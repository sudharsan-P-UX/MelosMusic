import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from users.models import User
from events.models import EventMaster, EventVenue, EventParticipant, EventAttendance

client = Client()

# Get a superadmin or teacher user to simulate session
user = User.objects.filter(is_active=True).first()
session = client.session
session['user_id'] = user.user_id
session.save()

print(f"Testing as user: {user.display_name or user.first_name} (ID: {user.user_id})")

# 1. Test GET on all submenus
tabs = ['calendar', 'list', 'upcoming', 'registration', 'assignments', 'venue', 'attendance', 'reports', 'details']

for t in tabs:
    res = client.get(f'/events/?tab={t}')
    assert res.status_code == 200, f"Failed GET for tab={t}: {res.status_code}"
    print(f"  [PASS] GET /events/?tab={t} returned 200 OK")

# 2. Test Venue CRUD actions
# A. Add Venue
res = client.post('/events/', {
    'action': 'add_venue',
    'venue_name': 'Test Acoustic Room',
    'capacity': 35,
    'address': 'Building D, Studio 4'
})
assert res.status_code in (200, 302), f"Failed add_venue: {res.status_code}"
v = EventVenue.objects.filter(venue_name='Test Acoustic Room').first()
assert v is not None, "Venue not created!"
print(f"  [PASS] POST action=add_venue created venue id={v.venue_id}")

# B. Edit Venue
res = client.post('/events/', {
    'action': 'edit_venue',
    'venue_id': v.venue_id,
    'venue_name': 'Updated Acoustic Room',
    'capacity': 50,
    'address': 'Building D, Studio 4 (Renovated)'
})
assert res.status_code in (200, 302), f"Failed edit_venue: {res.status_code}"
v.refresh_from_db()
assert v.venue_name == 'Updated Acoustic Room' and v.capacity == 50, "Venue update failed!"
print(f"  [PASS] POST action=edit_venue successfully updated venue")

# C. Delete Venue
res = client.post('/events/', {
    'action': 'delete_venue',
    'venue_id': v.venue_id
})
assert res.status_code in (200, 302), f"Failed delete_venue: {res.status_code}"
assert not EventVenue.objects.filter(venue_id=v.venue_id).exists(), "Venue deletion failed!"
print(f"  [PASS] POST action=delete_venue successfully removed venue")

# 3. Test Event CRUD actions
# A. Create Event
res = client.post('/events/', {
    'action': 'create_event',
    'event_name': 'Automated Test Jam Session',
    'event_type': 'Workshop',
    'event_date': '2026-11-15',
    'start_time': '14:00',
    'end_time': '16:00',
    'venue_id': '1',
    'status': '1',
    'description': 'A session to test automated event scheduling buttons.',
    'organizer': "Melo's Music",
    'contact_person': user.first_name,
    'contact_phone': '9988776655'
})
assert res.status_code in (200, 302), f"Failed create_event: {res.status_code}"
test_ev = EventMaster.objects.filter(event_name='Automated Test Jam Session').first()
assert test_ev is not None, "Event not created!"
print(f"  [PASS] POST action=create_event created event id={test_ev.event_id}")

# B. Edit Event
res = client.post('/events/', {
    'action': 'edit_event',
    'event_id': test_ev.event_id,
    'event_name': 'Automated Test Jam Session (Updated)',
    'event_type': 'Workshop',
    'event_date': '2026-11-16',
    'start_time': '15:00',
    'end_time': '17:00',
    'venue_id': '1',
    'status': '1',
    'description': 'Updated session description.',
    'organizer': "Melo's Music",
    'contact_person': user.first_name,
    'contact_phone': '9988776655'
})
assert res.status_code in (200, 302), f"Failed edit_event: {res.status_code}"
test_ev.refresh_from_db()
assert test_ev.event_name == 'Automated Test Jam Session (Updated)', "Event update failed!"
print(f"  [PASS] POST action=edit_event updated event id={test_ev.event_id}")

# 4. Test Participant Add and Delete
student = User.objects.filter(is_active=True, role__role_name__icontains='student').first()
res = client.post('/events/', {
    'action': 'add_participant',
    'event_id': test_ev.event_id,
    'user_id': student.user_id
})
assert res.status_code in (200, 302), f"Failed add_participant: {res.status_code}"
part = EventParticipant.objects.filter(event=test_ev, user=student).first()
assert part is not None, "Participant not added!"
print(f"  [PASS] POST action=add_participant added student to event")

# Delete Participant
res = client.post('/events/', {
    'action': 'delete_participant',
    'participant_id': part.event_participant_id,
    'event_id': test_ev.event_id
})
assert res.status_code in (200, 302), f"Failed delete_participant: {res.status_code}"
assert not EventParticipant.objects.filter(event_participant_id=part.event_participant_id).exists(), "Participant delete failed!"
print(f"  [PASS] POST action=delete_participant successfully removed participant")

# 5. Test Staff Assignment Add and Delete
teacher = User.objects.filter(is_active=True, role__role_name__icontains='teacher').first()
res = client.post('/events/', {
    'action': 'assign_staff',
    'event_id': test_ev.event_id,
    'user_id': teacher.user_id,
    'role_id': teacher.role_id
})
assert res.status_code in (200, 302), f"Failed assign_staff: {res.status_code}"
staff_p = EventParticipant.objects.filter(event=test_ev, user=teacher).first()
assert staff_p is not None, "Staff not assigned!"
print(f"  [PASS] POST action=assign_staff assigned teacher to event")

# Delete Staff Assignment
res = client.post('/events/', {
    'action': 'delete_staff_assignment',
    'participant_id': staff_p.event_participant_id
})
assert res.status_code in (200, 302), f"Failed delete_staff_assignment: {res.status_code}"
assert not EventParticipant.objects.filter(event_participant_id=staff_p.event_participant_id).exists(), "Staff delete failed!"
print(f"  [PASS] POST action=delete_staff_assignment successfully unassigned teacher")

# 6. Test Attendance Saving
# Add participant again for attendance test
part = EventParticipant.objects.create(event=test_ev, user=student)
res = client.post('/events/', {
    'action': 'save_attendance',
    'event_id': test_ev.event_id,
    f'attendance_status_{student.user_id}': '1', # Present
    f'remarks_{student.user_id}': 'Arrived on time, great performance'
})
assert res.status_code in (200, 302), f"Failed save_attendance: {res.status_code}"
att = EventAttendance.objects.filter(event=test_ev, user=student).first()
assert att is not None and att.attendance_status == 1, "Attendance save failed!"
print(f"  [PASS] POST action=save_attendance marked student as Present (status=1)")

# 7. Test Reports with Date & Type filters
res = client.get('/events/?tab=reports&from_date=2026-01-01&to_date=2026-12-31&type=Workshop')
assert res.status_code == 200, f"Failed reports filter: {res.status_code}"
print(f"  [PASS] GET /events/?tab=reports with filters returned 200 OK")

# Clean up test event and attendance
att.delete()
part.delete()
res = client.post('/events/', {
    'action': 'delete_event',
    'event_id': test_ev.event_id
})
assert res.status_code in (200, 302), f"Failed delete_event: {res.status_code}"
assert not EventMaster.objects.filter(event_id=test_ev.event_id).exists(), "Event deletion failed!"
print(f"  [PASS] POST action=delete_event successfully deleted event")

print("\nALL EVENT SCHEDULING SUBMENUS AND BUTTONS TESTED & WORKING PROPERLY!")
