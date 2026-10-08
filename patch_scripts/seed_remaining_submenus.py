import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

menus_to_seed = {
    'Student Profile': [
        {'name': 'Student Master', 'url': '/students/'},
        {'name': 'Enrollment Management', 'url': '/enrollment_management/'}
    ],
    'Attendance': [
        {'name': 'Student Attendance', 'url': '/attendance/student/'},
        {'name': 'Teacher Attendance', 'url': '/attendance/teacher/'}
    ],
    'Fees': [
        {'name': 'Fee Dashboard', 'url': '/fees/dashboard/'},
        {'name': 'Assign Fees', 'url': '/fees/assign/'},
        {'name': 'Fee Collection', 'url': '/fees/collection/'},
        {'name': 'Pending Fees', 'url': '/fees/pending/'},
        {'name': 'Receipts', 'url': '/fees/receipts/'},
        {'name': 'Refunds', 'url': '/fees/refunds/'},
        {'name': 'Fee Reports', 'url': '/fees/reports/'}
    ],
    'Event Scheduling': [
        {'name': 'Event List', 'url': '/events/?tab=upcoming'},
        {'name': 'Event Registration', 'url': '/events/?tab=registration'},
        {'name': 'Teacher Assignments', 'url': '/events/?tab=assignments'},
        {'name': 'Venue Management', 'url': '/events/?tab=venue'},
        {'name': 'Event Attendance', 'url': '/events/?tab=attendance'},
        {'name': 'Event Reports', 'url': '/events/?tab=reports'}
    ]
}

for parent_name, submenus in menus_to_seed.items():
    parent_menu = MasterMenu.objects.filter(menu_name=parent_name).first()
    if parent_menu:
        for sub in submenus:
            MasterMenu.objects.get_or_create(
                menu_name=sub['name'],
                defaults={
                    'url_page': sub['url'],
                    'parent_menu': parent_menu,
                    'is_active': True
                }
            )
        print(f"{parent_name} sub-menus seeded!")
    else:
        print(f"{parent_name} menu not found!")
