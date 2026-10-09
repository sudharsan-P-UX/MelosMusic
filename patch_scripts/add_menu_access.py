import re

with open('website/context_processors.py', 'r') as f:
    content = f.read()

new_processor = """
def current_menu_access_processor(request):
    if 'user_id' not in request.session:
        return {}
        
    try:
        from users.models import User, MasterMenu, RoleAccess
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        
        # If Superadmin, return all true
        if user.role.role_name == 'Superadmin':
            return {
                'menu_access': {
                    'view': True, 'add': True, 'edit': True, 'delete': True, 'export': True
                }
            }
            
        path = request.path
        
        # Find exact match first, then startswith as fallback
        menus = MasterMenu.objects.exclude(url_page='#').exclude(url_page='')
        current_menu = None
        
        for m in menus:
            # Handle special cases like /admin-dashboard/?tab=users
            # Since request.path is just /admin-dashboard/, we might need request.get_full_path()
            if m.url_page in request.get_full_path():
                current_menu = m
                break
                
        if not current_menu:
            for m in menus:
                if path.startswith(m.url_page):
                    current_menu = m
                    break
                
        if current_menu:
            access = RoleAccess.objects.get(role=user.role, menu=current_menu)
            return {
                'menu_access': {
                    'view': access.view_access,
                    'add': access.add_access,
                    'edit': access.edit_access,
                    'delete': access.delete_access,
                    'export': access.export_access
                }
            }
    except Exception as e:
        pass
        
    return {'menu_access': {'view': False, 'add': False, 'edit': False, 'delete': False, 'export': False}}
"""

if "def current_menu_access_processor" not in content:
    content += new_processor

with open('website/context_processors.py', 'w') as f:
    f.write(content)

with open('core/settings.py', 'r') as f:
    settings = f.read()

if "website.context_processors.current_menu_access_processor" not in settings:
    old_cp = "'website.context_processors.sidebar_menu_processor',"
    new_cp = "'website.context_processors.sidebar_menu_processor',\n                'website.context_processors.current_menu_access_processor',"
    settings = settings.replace(old_cp, new_cp)

with open('core/settings.py', 'w') as f:
    f.write(settings)
