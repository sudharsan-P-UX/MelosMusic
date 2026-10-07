import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_block = """            try:
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
                messages.success(request, f'Role permissions for {role.role_name} updated successfully!')
            except Exception as e:
                messages.error(request, 'Failed to update role permissions.')
                print(e)"""

new_block = """            try:
                # Optimized Bulk Operation to eliminate N+1 network latency
                role_access_instances = []
                for menu in menus:
                    m_id = str(menu.menu_id)
                    view = request.POST.get(f'view_{m_id}') == 'on'
                    add = request.POST.get(f'add_{m_id}') == 'on'
                    edit = request.POST.get(f'edit_{m_id}') == 'on'
                    delete = request.POST.get(f'delete_{m_id}') == 'on'
                    export = request.POST.get(f'export_{m_id}') == 'on'
                    
                    role_access_instances.append(
                        RoleAccess(
                            role=role, 
                            menu=menu,
                            view_access=view,
                            add_access=add,
                            edit_access=edit,
                            delete_access=delete,
                            export_access=export,
                            approve_access=False,
                            created_by=user.user_id
                        )
                    )
                
                # Update conflicts (Django 4.1+) natively translates this to a single UPSERT query
                RoleAccess.objects.bulk_create(
                    role_access_instances,
                    update_conflicts=True,
                    unique_fields=['role', 'menu'],
                    update_fields=['view_access', 'add_access', 'edit_access', 'delete_access', 'export_access', 'created_by']
                )
                messages.success(request, f'Role permissions for {role.role_name} updated successfully!')
            except Exception as e:
                messages.error(request, 'Failed to update role permissions.')
                print(e)"""

content = content.replace(old_block, new_block)

with open('website/views.py', 'w') as f:
    f.write(content)
