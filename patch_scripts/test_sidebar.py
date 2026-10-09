import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User, MasterMenu, RoleAccess

user = User.objects.get(first_name='Superadmin') # Assuming username is superadmin
print(f"User role: {user.role.role_name}")

all_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
access_records = RoleAccess.objects.filter(role=user.role, view_access=True).values_list('menu_id', flat=True)
access_set = set(access_records)

def build_tree(parent_id=None):
    tree = []
    for m in all_menus:
        if m.parent_menu_id == parent_id:
            children = build_tree(m.menu_id)
            if m.menu_id in access_set or len(children) > 0:
                m.children = children
                tree.append(m)
    return tree

top_menus = build_tree(None)
for m in top_menus:
    print(f"- {m.menu_name} (id={m.menu_id}) (children={len(m.children)})")
    for c in m.children:
        print(f"  - {c.menu_name} (id={c.menu_id}) (children={len(c.children)})")
        for sc in c.children:
            print(f"    - {sc.menu_name} (id={sc.menu_id})")
