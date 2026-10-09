import re

with open('website/views.py', 'r') as f:
    content = f.read()

new_action = """        if action == 'save_menu_orders':
            if not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            
            for key, value in request.POST.items():
                if key.startswith('order_'):
                    menu_id = key.replace('order_', '')
                    try:
                        menu = MasterMenu.objects.get(menu_id=menu_id)
                        menu.display_order = int(value)
                        menu.save()
                    except Exception as e:
                        pass
            
            messages.success(request, 'Menu order updated successfully!')
            return redirect('/admin-dashboard/?tab=menu')

        if action == 'save_menu':"""

content = content.replace("        if action == 'save_menu':", new_action)

with open('website/views.py', 'w') as f:
    f.write(content)
