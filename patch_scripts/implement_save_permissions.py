import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Replace admin_dashboard_view
parts = content.split('def admin_dashboard_view(request):')
prefix = parts[0]

correct_view = """def admin_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    from users.models import Role, RoleGroup, RoleAccess, MasterMenu
    
    roles = Role.objects.all().select_related('role_group')
    users = User.objects.all().select_related('role')
    menus = MasterMenu.objects.filter(is_active=True).order_by('menu_id')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_user':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            role_id = request.POST.get('role_id')
            
            try:
                role = Role.objects.get(role_id=role_id)
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role
                )
            except Exception as e:
                print(e)
            return redirect('/admin-dashboard/?tab=users')
            
        elif action == 'save_permissions':
            role_id = request.POST.get('role_id')
            role = Role.objects.get(role_id=role_id)
            for menu in menus:
                m_id = str(menu.menu_id)
                view = request.POST.get(f'view_{m_id}') == 'on'
                add = request.POST.get(f'add_{m_id}') == 'on'
                edit = request.POST.get(f'edit_{m_id}') == 'on'
                delete = request.POST.get(f'delete_{m_id}') == 'on'
                export = request.POST.get(f'export_{m_id}') == 'on'
                
                RoleAccess.objects.update_or_create(
                    role=role, menu=menu,
                    defaults={
                        'view_access': view,
                        'add_access': add,
                        'edit_access': edit,
                        'delete_access': delete,
                        'export_access': export,
                        'created_by': user.user_id
                    }
                )
            return redirect(f'/admin-dashboard/?tab=roles&role_id={role_id}')

    tab = request.GET.get('tab', 'dashboard')
    
    # Selected role for permissions matrix
    selected_role_id = request.GET.get('role_id')
    selected_role = None
    role_access_map = {}
    if roles.exists():
        if not selected_role_id:
            selected_role_id = roles.first().role_id
        
        try:
            selected_role = Role.objects.get(role_id=selected_role_id)
            access_records = RoleAccess.objects.filter(role=selected_role)
            for access in access_records:
                role_access_map[access.menu_id] = access
        except Role.DoesNotExist:
            selected_role = roles.first()
    
    from users.models import UserLoginDetails
    audit_logs = UserLoginDetails.objects.select_related('user').order_by('-login_date')[:50]
    
    context = {
        'page_title': 'Admin',
        'active_tab': tab,
        'user': user,
        'roles': roles,
        'users': users,
        'menus': menus,
        'audit_logs': audit_logs,
        'selected_role': selected_role,
        'role_access_map': role_access_map,
    }
    return render(request, 'website/admin_dashboard.html', context)
"""

with open('website/views.py', 'w') as f:
    f.write(prefix + correct_view)
