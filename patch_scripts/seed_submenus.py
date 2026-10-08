import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# Find the Admin menu
admin_menu = MasterMenu.objects.filter(menu_name='Admin').first()
if admin_menu:
    submenus = [
        {'name': 'Admin Dashboard', 'url': '/admin-dashboard/?tab=dashboard'},
        {'name': 'User Management', 'url': '/admin-dashboard/?tab=users'},
        {'name': 'Role Management', 'url': '/admin-dashboard/?tab=roles'},
        {'name': 'Menu Permissions', 'url': '/admin-dashboard/?tab=menu'},
        {'name': 'System Settings', 'url': '/admin-dashboard/?tab=settings'},
        {'name': 'Audit Logs', 'url': '/admin-dashboard/?tab=audit'},
    ]
    
    for sub in submenus:
        MasterMenu.objects.get_or_create(
            menu_name=sub['name'],
            defaults={
                'url_page': sub['url'],
                'parent_menu': admin_menu,
                'is_active': True
            }
        )
    print("Admin sub-menus seeded!")
else:
    print("Admin menu not found!")
