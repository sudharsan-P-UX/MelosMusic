import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# 1. Create Administration Menu
admin_menu, _ = MasterMenu.objects.get_or_create(menu_name='Administration', defaults={'is_active': True})
admin_menu.parent_menu = None
admin_menu.save()

# 2. Re-parent existing menus
to_reparent = ['Dashboard', 'Fees', 'Courses & Batches', 'Event Scheduling', 'Timetable']
for name in to_reparent:
    menu = MasterMenu.objects.filter(menu_name=name).first()
    if menu:
        menu.parent_menu = admin_menu
        menu.save()
        print(f"Reparented {name} -> Administration")

# 3. Create new menus under Administration
MasterMenu.objects.get_or_create(
    menu_name='Student Course Allocation',
    defaults={'url_page': '/page/student-course-allocation/', 'parent_menu': admin_menu, 'is_active': True}
)

MasterMenu.objects.get_or_create(
    menu_name='Teacher Class Allocation',
    defaults={'url_page': '/page/teacher-class-allocation/', 'parent_menu': admin_menu, 'is_active': True}
)

print("Administration menu successfully created and structured!")
