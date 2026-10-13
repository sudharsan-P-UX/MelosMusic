import os
import sys
import django
from datetime import date, time, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from events.models import EventMaster, EventVenue, EventParticipant, EventAttendance
from users.models import User, Role

def run():
    print("Seeding initial Event Scheduling sample data...")

    # 1. Venues
    venues_data = [
        {"venue_name": "Main Auditorium", "capacity": 500, "address": "Block A, Main Campus"},
        {"venue_name": "Studio 101 (Sound Lab)", "capacity": 45, "address": "Block C, 1st Floor"},
        {"venue_name": "Open Air Amphitheatre", "capacity": 300, "address": "Central Garden Campus"},
    ]
    venues = []
    for vd in venues_data:
        v, created = EventVenue.objects.get_or_create(venue_name=vd["venue_name"], defaults=vd)
        venues.append(v)
        if created:
            print(f"Created venue: {v.venue_name}")

    # 2. Events
    admin_user = User.objects.filter(role__role_name__iexact='superadmin').first() or User.objects.first()
    today = date.today()

    events_data = [
        {
            "event_name": "Annual Music Day Celebration",
            "event_type": "Performance",
            "event_date": today + timedelta(days=12),
            "start_time": time(17, 0),
            "end_time": time(20, 30),
            "venue": venues[0],
            "description": "Grand annual concert showcasing classical, fusion, and contemporary performances by all students and staff.",
            "status": 1, # Upcoming
            "organizer": "Melo's Music Academy",
            "contact_person": "Sudharsan P",
            "contact_phone": "9876543210",
            "max_participants": 200,
        },
        {
            "event_name": "Guitar & Bass Masterclass",
            "event_type": "Workshop",
            "event_date": today + timedelta(days=5),
            "start_time": time(10, 0),
            "end_time": time(13, 0),
            "venue": venues[1],
            "description": "Hands-on masterclass focusing on fretboard mastery, modal improvisation, and tone shaping.",
            "status": 1, # Upcoming
            "organizer": "Melo's Guitar Department",
            "contact_person": "Kavitha S",
            "contact_phone": "9876543211",
            "max_participants": 40,
        },
        {
            "event_name": "Classical Vocal Recital",
            "event_type": "Performance",
            "event_date": today - timedelta(days=7),
            "start_time": time(16, 30),
            "end_time": time(19, 0),
            "venue": venues[2],
            "description": "Evening ragas recital featuring senior academy vocal students and visiting guest artists.",
            "status": 2, # Completed
            "organizer": "Vocal Arts Guild",
            "contact_person": "Ramesh N",
            "contact_phone": "9876543212",
            "max_participants": 100,
        },
    ]

    events = []
    for ed in events_data:
        e, created = EventMaster.objects.get_or_create(
            event_name=ed["event_name"],
            defaults={**ed, "created_by": admin_user}
        )
        events.append(e)
        if created:
            print(f"Created event: {e.event_name}")

    # 3. Participants & Staff Assignments
    students = list(User.objects.filter(is_active=True, role__role_name__icontains='student'))
    teachers = list(User.objects.filter(is_active=True, role__role_name__icontains='teacher'))
    student_role = Role.objects.filter(role_name__icontains='student').first()
    teacher_role = Role.objects.filter(role_name__icontains='teacher').first()

    for ev in events:
        for s in students[:3]:
            EventParticipant.objects.get_or_create(event=ev, user=s, defaults={"role": student_role})
        for t in teachers[:2]:
            EventParticipant.objects.get_or_create(event=ev, user=t, defaults={"role": teacher_role})

    # 4. Attendance for completed event
    completed_event = events[2]
    participants = EventParticipant.objects.filter(event=completed_event)
    for idx, p in enumerate(participants):
        status = 1 if idx % 4 != 0 else 2 # Mostly present, some absent
        EventAttendance.objects.get_or_create(
            event=completed_event,
            user=p.user,
            defaults={"attendance_status": status, "remarks": "Checked-in" if status == 1 else "Absent"}
        )

    print("Seeding completed successfully!")

if __name__ == '__main__':
    run()
