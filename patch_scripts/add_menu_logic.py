import re

with open('website/views.py', 'r') as f:
    content = f.read()

menu_post_logic = """
        elif action == 'save_menu':
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
                    messages.success(request, f'Menu {menu_name} created successfully!')
            except Exception as e:
                messages.error(request, 'Failed to save menu.')
                print(e)
            return redirect('/admin-dashboard/?tab=menu')
            
        elif action == 'delete_menu':
            menu_id = request.POST.get('menu_id')
            try:
                menu = MasterMenu.objects.get(menu_id=menu_id)
                menu_name = menu.menu_name
                menu.delete()
                messages.success(request, f'Menu {menu_name} deleted successfully!')
            except Exception as e:
                messages.error(request, 'Failed to delete menu.')
            return redirect('/admin-dashboard/?tab=menu')
"""

if "elif action == 'save_menu':" not in content:
    content = content.replace("tab = request.GET.get('tab', 'dashboard')", menu_post_logic + "\n    tab = request.GET.get('tab', 'dashboard')")

with open('website/views.py', 'w') as f:
    f.write(content)
