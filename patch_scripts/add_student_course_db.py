import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu, Role, RoleAccess

student_profile = MasterMenu.objects.filter(menu_name='Student Profile').first()

student_course, _ = MasterMenu.objects.get_or_create(
    menu_name='Student Course',
    defaults={'url_page': '/student-course/', 'parent_menu': student_profile, 'is_active': True}
)

superadmin_role = Role.objects.filter(role_name='Superadmin').first()
if superadmin_role:
    RoleAccess.objects.update_or_create(
        role=superadmin_role,
        menu=student_course,
        defaults={
            'view_access': True,
            'add_access': True,
            'edit_access': True,
            'delete_access': True,
            'export_access': True,
        }
    )
print("Student Course menu added to DB and permissions granted.")
