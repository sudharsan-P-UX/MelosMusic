import re

with open('website/views.py', 'r') as f:
    content = f.read()

# 1. Update save_menu in admin_dashboard_view to include display_order
old_save_menu = """        if action == 'save_menu':
            menu_id = request.POST.get('menu_id')
            menu_name = request.POST.get('menu_name')
            url_page = request.POST.get('url_page')
            is_active = request.POST.get('is_active') == 'on'"""

new_save_menu = """        if action == 'save_menu':
            menu_id = request.POST.get('menu_id')
            menu_name = request.POST.get('menu_name')
            url_page = request.POST.get('url_page')
            is_active = request.POST.get('is_active') == 'on'
            display_order = request.POST.get('display_order', 0)
            try:
                display_order = int(display_order)
            except ValueError:
                display_order = 0"""

content = content.replace(old_save_menu, new_save_menu)

old_save_menu_create = """                    menu.menu_name = menu_name
                    menu.url_page = url_page
                    menu.is_active = is_active
                    menu.save()"""

new_save_menu_create = """                    menu.menu_name = menu_name
                    menu.url_page = url_page
                    menu.is_active = is_active
                    menu.display_order = display_order
                    menu.save()"""

content = content.replace(old_save_menu_create, new_save_menu_create)

old_save_menu_insert = """                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        is_active=is_active
                    )"""

new_save_menu_insert = """                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        is_active=is_active,
                        display_order=display_order
                    )"""

content = content.replace(old_save_menu_insert, new_save_menu_insert)

# 2. Update menu sorting in admin_dashboard_view
old_sort = """raw_menus = list(MasterMenu.objects.filter(is_active=True).order_by('menu_id'))"""
new_sort = """raw_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))"""
content = content.replace(old_sort, new_sort)

with open('website/views.py', 'w') as f:
    f.write(content)
