import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import Role, MasterMenu, RoleAccess

superadmin_roles = Role.objects.filter(role_name__iexact='Superadmin')
if superadmin_roles.exists():
    superadmin = superadmin_roles.first()
    menus = MasterMenu.objects.all()
    for menu in menus:
        RoleAccess.objects.update_or_create(
            role=superadmin,
            menu=menu,
            defaults={
                'view_access': True,
                'add_access': True,
                'edit_access': True,
                'delete_access': True,
                'export_access': True,
                'approve_access': True,
                'created_by': 1 # Assuming Superadmin has user_id 1
            }
        )
    print("Superadmin permissions seeded!")
else:
    print("Superadmin role not found.")
