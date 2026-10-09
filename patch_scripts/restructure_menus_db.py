import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# 1. Rename Teacher Management to Teacher Profile (Parent)
teacher_profile = MasterMenu.objects.filter(menu_name='Teacher Management', parent_menu__isnull=True).first()
if teacher_profile:
    teacher_profile.menu_name = 'Teacher Profile'
    teacher_profile.save()
else:
    # Maybe it was already renamed or doesn't exist
    teacher_profile = MasterMenu.objects.filter(menu_name='Teacher Profile').first()
    if not teacher_profile:
        teacher_profile = MasterMenu.objects.create(menu_name='Teacher Profile', is_active=True)

# 2. Add Teacher Master submenu
teacher_master, _ = MasterMenu.objects.get_or_create(
    menu_name='Teacher Master',
    defaults={'url_page': '/teachers/', 'parent_menu': teacher_profile, 'is_active': True}
)
# Ensure parent is correct in case it already existed
teacher_master.parent_menu = teacher_profile
teacher_master.save()

# 3. Move Student Attendance to Student Profile
student_profile = MasterMenu.objects.filter(menu_name='Student Profile').first()
student_attendance = MasterMenu.objects.filter(menu_name='Student Attendance').first()
if student_attendance and student_profile:
    student_attendance.parent_menu = student_profile
    student_attendance.save()

# 4. Move Teacher Attendance to Teacher Profile
teacher_attendance = MasterMenu.objects.filter(menu_name='Teacher Attendance').first()
if teacher_attendance and teacher_profile:
    teacher_attendance.parent_menu = teacher_profile
    teacher_attendance.save()

# 5. Remove Attendance Parent Menu (if empty)
attendance_parent = MasterMenu.objects.filter(menu_name='Attendance', parent_menu__isnull=True).first()
if attendance_parent:
    # Check if it has any children left
    if not MasterMenu.objects.filter(parent_menu=attendance_parent).exists():
        attendance_parent.delete()

print("Database Menu Structure Updated!")
