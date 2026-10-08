import re

with open('website/views.py', 'r') as f:
    content = f.read()

rbac_logic = """
    roles = Role.objects.all().select_related('role_group')
    users = User.objects.all().select_related('role')
    menus = MasterMenu.objects.filter(is_active=True).order_by('menu_id')
    
    # RBAC Enforcement
    try:
        admin_menu = MasterMenu.objects.get(menu_name='Admin')
        admin_access = RoleAccess.objects.get(role=user.role, menu=admin_menu)
    except (MasterMenu.DoesNotExist, RoleAccess.DoesNotExist):
        admin_access = None

    if not admin_access or not admin_access.view_access:
        messages.error(request, 'You do not have permission to view the Admin Dashboard.')
        return redirect('index')
"""

old_setup = """
    roles = Role.objects.all().select_related('role_group')
    users = User.objects.all().select_related('role')
    menus = MasterMenu.objects.filter(is_active=True).order_by('menu_id')
"""

content = content.replace(old_setup, rbac_logic)


action_logic = """    if request.method == 'POST':
        action = request.POST.get('action')
        
        # RBAC Check for POST actions
        if action == 'create_user' and not admin_access.add_access:
            messages.error(request, 'You do not have permission to add records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_permissions' and not admin_access.edit_access:
            messages.error(request, 'You do not have permission to edit records.')
            return redirect('/admin-dashboard/')
            
        if action == 'save_menu':
            if request.POST.get('menu_id') and not admin_access.edit_access:
                messages.error(request, 'You do not have permission to edit records.')
                return redirect('/admin-dashboard/?tab=menu')
            elif not request.POST.get('menu_id') and not admin_access.add_access:
                messages.error(request, 'You do not have permission to add records.')
                return redirect('/admin-dashboard/?tab=menu')
                
        if action == 'delete_menu' and not admin_access.delete_access:
            messages.error(request, 'You do not have permission to delete records.')
            return redirect('/admin-dashboard/?tab=menu')
"""

old_action_logic = """    if request.method == 'POST':
        action = request.POST.get('action')"""

content = content.replace(old_action_logic, action_logic)


with open('website/views.py', 'w') as f:
    f.write(content)
