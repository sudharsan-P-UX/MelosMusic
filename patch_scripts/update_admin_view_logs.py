import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_context = """    context = {
        'page_title': 'Admin',
        'active_tab': tab,
        'user': user,
        'roles': roles,
        'users': users,
        'menus': menus,
    }"""

new_context = """    from users.models import UserLoginDetails
    audit_logs = UserLoginDetails.objects.select_related('user').order_by('-login_date')[:50]
    
    context = {
        'page_title': 'Admin',
        'active_tab': tab,
        'user': user,
        'roles': roles,
        'users': users,
        'menus': menus,
        'audit_logs': audit_logs,
    }"""

content = content.replace(old_context, new_context)

with open('website/views.py', 'w') as f:
    f.write(content)
