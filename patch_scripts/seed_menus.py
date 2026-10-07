import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

menus = [
    "Dashboard",
    "Student Profile",
    "Attendance",
    "Fees",
    "Event Scheduling",
    "Courses & Batches",
    "Teacher Management",
    "Timetable",
    "Notifications",
    "Admin"
]

def seed_menus():
    for m in menus:
        menu, created = MasterMenu.objects.get_or_create(
            menu_name=m,
            defaults={'url_page': '#'}
        )
        if created:
            print(f"Created menu: {m}")
        else:
            print(f"Menu exists: {m}")

if __name__ == '__main__':
    seed_menus()
