import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Add messages import if not exists
if 'from django.contrib import messages' not in content:
    content = content.replace('from django.shortcuts import render, redirect', 'from django.shortcuts import render, redirect\nfrom django.contrib import messages')

# In save_permissions:
old_save_block = """            for menu in menus:
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
            return redirect(f'/admin-dashboard/?tab=roles&role_id={role_id}')"""

new_save_block = """            try:
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
                print(e)
            return redirect(f'/admin-dashboard/?tab=roles&role_id={role_id}')"""

content = content.replace(old_save_block, new_save_block)

# Add messages to create_user too
old_create_user = """                User.objects.create(
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
            return redirect('/admin-dashboard/?tab=users')"""

new_create_user = """                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role
                )
                messages.success(request, f'User {first_name} {last_name} created successfully!')
            except Exception as e:
                messages.error(request, 'Failed to create user.')
                print(e)
            return redirect('/admin-dashboard/?tab=users')"""

content = content.replace(old_create_user, new_create_user)

with open('website/views.py', 'w') as f:
    f.write(content)
