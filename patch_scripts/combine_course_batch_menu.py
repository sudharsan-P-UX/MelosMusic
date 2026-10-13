import os
import sys
import django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu, RoleAccess, MenuColumn

def run():
    print("Combining Course and Batches menu...")
    
    # 1. Update menu 6 name to "Course and Batches"
    menu_6 = MasterMenu.objects.filter(menu_id=6).first()
    if menu_6:
        menu_6.menu_name = "Course and Batches"
        menu_6.save()
        print(f"Updated Menu 6: name={menu_6.menu_name}, url={menu_6.url_page}, parent_id={menu_6.parent_menu_id}")
    else:
        print("Menu 6 not found!")
    
    # 2. Check submenus of menu 6
    submenus = list(MasterMenu.objects.filter(parent_menu_id=6))
    print(f"Found {len(submenus)} submenus under menu 6: {[m.menu_name for m in submenus]}")
    
    # 3. Delete submenus 53, 54, 55 (and any other submenus of menu 6)
    for sm in submenus:
        print(f"Deleting submenu {sm.menu_id}: {sm.menu_name}")
        sm.delete()
        
    # Also specifically check ids 53, 54, 55 if they were reparented somehow
    extra = MasterMenu.objects.filter(menu_id__in=[53, 54, 55])
    for em in extra:
        print(f"Deleting extra menu {em.menu_id}: {em.menu_name}")
        em.delete()

    print("\nVerification:")
    remaining_submenus = MasterMenu.objects.filter(parent_menu_id=6).count()
    print(f"Submenus remaining under menu 6: {remaining_submenus}")
    
    menu_6_after = MasterMenu.objects.filter(menu_id=6).first()
    print(f"Menu 6 after update: id={menu_6_after.menu_id}, name='{menu_6_after.menu_name}', parent={menu_6_after.parent_menu_id}, url='{menu_6_after.url_page}'")
    
    # Role access for menu 6
    for ra in RoleAccess.objects.filter(menu_id=6):
        print(f"Role: {ra.role.role_name} -> view={ra.view_access}, add={ra.add_access}, edit={ra.edit_access}, delete={ra.delete_access}")

if __name__ == '__main__':
    run()
