import json
import os
from django.conf import settings

def security_settings(request):
    security = {
        'phone_length': 10,
        'email_length': 255,
        'password_expire': 90,
        'attendance_from_date': '2026-09-05',
        'attendance_to_date': '2026-10-05',
    }
    try:
        path = os.path.join(settings.BASE_DIR, 'security_settings.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                security.update(data)
    except:
        pass
    return {'security_settings': security}

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
        if user.role and user.role.role_name.lower() == 'superadmin':
            access_set = {m.menu_id for m in all_menus}
        else:
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
        from users.models import User, RoleAccess, MasterMenu
        user = User.objects.get(user_id=request.session['user_id'])
        if not user.role:
            return {'user_perms': {}}
            
        if user.role and user.role.role_name.lower() == 'superadmin':
            perms = {}
            for menu in MasterMenu.objects.filter(is_active=True):
                menu_name = menu.menu_name.replace(' ', '_').replace('&', 'and')
                perms[menu_name] = {
                    'view': True,
                    'add': True,
                    'edit': True,
                    'delete': True,
                    'export': True,
                }
            return {'user_perms': perms}
            
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
        if user.role and user.role.role_name.lower() == 'superadmin':
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


def menu_columns_processor(request):
    """
    Context processor that provides configured table columns for each menu.
    Allows templates to dynamically order, label, and toggle columns.
    """
    try:
        from users.models import MenuColumn
        active_cols = list(
            MenuColumn.objects.filter(status=True, menu__is_active=True)
            .select_related('menu')
            .order_by('order_by', 'column_id')
        )
        
        columns_by_name = {}
        for col in active_cols:
            m_name = col.menu.menu_name
            # Exact name
            columns_by_name.setdefault(m_name, []).append(col)
            # Normalized key: 'Staff Master' -> 'staff_master'
            norm_key = m_name.lower().replace(' ', '_').replace('&', 'and').replace('-', '_')
            columns_by_name.setdefault(norm_key, []).append(col)
            if 'staff' in norm_key:
                columns_by_name.setdefault(norm_key.replace('staff', 'teacher'), []).append(col)
            elif 'teacher' in norm_key:
                columns_by_name.setdefault(norm_key.replace('teacher', 'staff'), []).append(col)
            # URL mapping
            if col.menu.url_page:
                columns_by_name.setdefault(col.menu.url_page, []).append(col)
                # Tab mapping if url has ?tab=
                if '?tab=' in col.menu.url_page:
                    tab_val = col.menu.url_page.split('?tab=')[-1].split('&')[0]
                    columns_by_name.setdefault(f"tab_{tab_val}", []).append(col)

        # Current page columns
        current_cols = []
        full_path = request.get_full_path()
        path = request.path
        for url_key, c_list in columns_by_name.items():
            if url_key.startswith('/') and (url_key in full_path or (url_key != '/' and path.startswith(url_key))):
                current_cols = c_list
                break

        return {
            'menu_columns_map': columns_by_name,
            'current_menu_columns': current_cols,
        }
    except Exception as e:
        return {'menu_columns_map': {}, 'current_menu_columns': []}
