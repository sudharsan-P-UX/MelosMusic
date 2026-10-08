import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_save_menu = """        if action == 'save_menu':
            if request.POST.get('menu_id') and not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            elif not request.POST.get('menu_id') and not admin_access.add_access:
                messages.error(request, 'You do not have permission to add records.')
                return redirect('/admin-dashboard/?tab=menu')
                
        if action == 'delete_menu' and not admin_access.delete_access:
            messages.error(request, 'You do not have permission to delete records.')
            return redirect('/admin-dashboard/?tab=menu')
            
        if action == 'save_menu':
            menu_id = request.POST.get('menu_id')
            menu_name = request.POST.get('menu_name')
            url_page = request.POST.get('url_page')
            is_active = request.POST.get('is_active') == 'on'
            
            try:
                if menu_id:
                    menu = MasterMenu.objects.get(menu_id=menu_id)
                    menu.menu_name = menu_name
                    menu.url_page = url_page
                    menu.is_active = is_active
                    menu.save()
                    messages.success(request, f'Menu {menu_name} updated successfully!')
                else:
                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        is_active=is_active
                    )
                    messages.success(request, f'Menu {menu_name} created successfully!')"""

new_save_menu = """        if action == 'save_menu':
            if request.POST.get('menu_id') and not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            elif not request.POST.get('menu_id') and not admin_access.add_access:
                messages.error(request, 'You do not have permission to add records.')
                return redirect('/admin-dashboard/?tab=menu')
                
        if action == 'delete_menu' and not admin_access.delete_access:
            messages.error(request, 'You do not have permission to delete records.')
            return redirect('/admin-dashboard/?tab=menu')
            
        if action == 'save_menu':
            menu_id = request.POST.get('menu_id')
            menu_name = request.POST.get('menu_name')
            url_page = request.POST.get('url_page')
            parent_menu_id = request.POST.get('parent_menu_id')
            is_active = request.POST.get('is_active') == 'on'
            
            try:
                parent_menu = MasterMenu.objects.get(menu_id=parent_menu_id) if parent_menu_id else None
                if menu_id:
                    menu = MasterMenu.objects.get(menu_id=menu_id)
                    menu.menu_name = menu_name
                    menu.url_page = url_page
                    menu.parent_menu = parent_menu
                    menu.is_active = is_active
                    menu.save()
                    messages.success(request, f'Menu {menu_name} updated successfully!')
                else:
                    MasterMenu.objects.create(
                        menu_name=menu_name,
                        url_page=url_page,
                        parent_menu=parent_menu,
                        is_active=is_active
                    )
                    messages.success(request, f'Menu {menu_name} created successfully!')"""

content = content.replace(old_save_menu, new_save_menu)

with open('website/views.py', 'w') as f:
    f.write(content)
