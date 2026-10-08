import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_menu_fetch = "menus = MasterMenu.objects.filter(is_active=True).order_by('menu_id')"

new_menu_fetch = """# Fetch menus and construct a tree (Parents first, then their children)
    raw_menus = list(MasterMenu.objects.filter(is_active=True).order_by('menu_id'))
    menus = []
    for m in raw_menus:
        if not m.parent_menu_id:
            menus.append(m)
            # Find children for this parent
            for child in raw_menus:
                if child.parent_menu_id == m.menu_id:
                    menus.append(child)"""

content = content.replace(old_menu_fetch, new_menu_fetch)

with open('website/views.py', 'w') as f:
    f.write(content)
