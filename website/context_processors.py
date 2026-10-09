from users.models import MasterMenu

def sidebar_menu_processor(request):
    if 'user_id' not in request.session:
        return {'sidebar_menus': []}
        
    try:
        from users.models import User, RoleAccess
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        
        # Get all menus
        all_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
        
        # Get role access for this user
        access_records = RoleAccess.objects.filter(role=user.role, view_access=True).values_list('menu_id', flat=True)
        access_set = set(access_records)
        
        # Build tree
        def build_tree(parent_id=None):
            tree = []
            for m in all_menus:
                if m.parent_menu_id == parent_id:
                    # Recursively build children first
                    children = build_tree(m.menu_id)
                    # Include this menu if it's explicitly accessible, or if it has accessible children
                    if m.menu_id in access_set or len(children) > 0:
                        m.children = children
                        tree.append(m)
            return tree

        top_menus = build_tree(None)
        
        return {'sidebar_menus': top_menus}
    except Exception as e:
        print(f"Error in context processor: {e}")
        return {'sidebar_menus': []}

def user_permissions(request):
    if 'user_id' not in request.session:
        return {'user_perms': {}}
        
    try:
        from users.models import User, RoleAccess
        user = User.objects.get(user_id=request.session['user_id'])
        if not user.role:
            return {'user_perms': {}}
            
        accesses = RoleAccess.objects.filter(role=user.role).select_related('menu')
        perms = {}
        for access in accesses:
            # e.g. "Student Profile" -> "Student_Profile"
            menu_name = access.menu.menu_name.replace(' ', '_').replace('&', 'and')
            perms[menu_name] = {
                'view': access.view_access,
                'add': access.add_access,
                'edit': access.edit_access,
                'delete': access.delete_access,
                'export': access.export_access,
            }
        return {'user_perms': perms}
    except Exception as e:
        print(f"Error loading user perms: {e}")
        return {'user_perms': {}}

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
