import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu, RoleAccess, Role

def run():
    # Check if it exists
    menu = MasterMenu.objects.filter(menu_name='Audit Logs').first()
    if not menu:
        menu = MasterMenu.objects.create(
            menu_name='Audit Logs',
            url_page='/audit-logs/',
            display_order=90,
            is_active=True
        )
        print("Created Audit Logs menu.")
    else:
        menu.url_page = '/audit-logs/'
        menu.is_active = True
        menu.parent_menu_id = None # Ensure it's top-level
        menu.save()
        print("Updated Audit Logs menu.")

    # Grant superadmin access
    superadmin = Role.objects.filter(role_name='Superadmin').first()
    if superadmin:
        ra, created = RoleAccess.objects.get_or_create(role=superadmin, menu=menu)
        ra.view_access = True
        ra.save()
        print("Granted superadmin access.")

if __name__ == '__main__':
    run()
