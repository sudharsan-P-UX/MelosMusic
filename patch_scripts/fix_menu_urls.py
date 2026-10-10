import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# Fix Timetable
menu = MasterMenu.objects.filter(menu_name='Timetable').first()
if menu:
    menu.url_page = '/timetable/'
    menu.save()

# Fix Notifications
menu = MasterMenu.objects.filter(menu_name='Notifications').first()
if menu:
    menu.url_page = '/page/notifications/'
    menu.save()

# Fix the child 'Attendance' (id=47)
menu = MasterMenu.objects.filter(menu_name='Attendance', parent_menu__isnull=False).first()
if menu:
    menu.url_page = '/attendance-log/'
    menu.save()

# Make 'Fees' and 'Event Scheduling' have a dashboard url so clicking them directly also navigates
menu = MasterMenu.objects.filter(menu_name='Fees').first()
if menu:
    menu.url_page = '/fees/dashboard/'
    menu.save()

menu = MasterMenu.objects.filter(menu_name='Event Scheduling').first()
if menu:
    menu.url_page = '/events/'
    menu.save()

print("Database menus updated.")
