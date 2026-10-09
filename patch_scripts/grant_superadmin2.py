import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import Role, MasterMenu, RoleAccess

superadmin_role = Role.objects.filter(role_name='Superadmin').first()
if superadmin_role:
    all_menus = MasterMenu.objects.all()
    for m in all_menus:
        RoleAccess.objects.update_or_create(
            role=superadmin_role,
            menu=m,
            defaults={
                'view_access': True,
                'add_access': True,
                'edit_access': True,
                'delete_access': True,
                'export_access': True,
            }
        )
    print("Superadmin granted full access to all menus!")
