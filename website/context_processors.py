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

def resolve_current_menu(request):
    """
    Resolves the active MasterMenu for the given request URL,
    prioritizing exact matches with query parameters before prefix matches.
    """
    try:
        from users.models import MasterMenu
        full_path = request.get_full_path()
        path = request.path

        menus = list(MasterMenu.objects.filter(is_active=True).exclude(url_page='#').exclude(url_page=''))

        # 1. Exact full_path match (e.g. /courses/?tab=courses)
        for m in menus:
            if m.url_page and m.url_page.strip() == full_path.strip():
                return m

        # 2. Query param match (e.g. /courses/?tab=batches when full_path has ?tab=batches&...)
        for m in menus:
            if '?' in m.url_page:
                base_url, query = m.url_page.split('?', 1)
                if path.rstrip('/') == base_url.rstrip('/') and query in full_path:
                    return m

        # 3. Exact path match (excluding root '/')
        for m in menus:
            if m.url_page != '/' and m.url_page.rstrip('/') == path.rstrip('/'):
                return m

        # 4. Longest prefix match for action URLs (e.g. /students/delete/18/, /students/update/18/ -> /students/)
        prefix_matches = [
            m for m in menus 
            if m.url_page != '/' and (
                path.startswith(m.url_page.rstrip('/') + '/') or 
                path.rstrip('/').startswith(m.url_page.split('?')[0].rstrip('/'))
            )
        ]
        if prefix_matches:
            return max(prefix_matches, key=lambda m: len(m.url_page))

        # 5. Root path match
        if path == '/':
            for m in menus:
                if m.url_page == '/':
                    return m
    except Exception as e:
        print(f"Error resolving current menu: {e}")
    return None

def has_permission(request, action='view', menu_identifier=None, parent_fallback=None):
    """
    Checks if the current session user has permission for the specified action.
    action: 'view', 'add', 'edit', 'delete', 'export'
    menu_identifier: Optional MasterMenu instance, menu_id (int), menu_name (str), or url_page (str).
                     If None, resolves from request.
    parent_fallback: Optional menu identifier to check if no explicit RoleAccess row exists for menu_identifier.
    """
    if 'user_id' not in request.session:
        return False
    try:
        from users.models import User, RoleAccess, MasterMenu
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        if not user.role:
            return False

        menu = None
        if isinstance(menu_identifier, MasterMenu):
            menu = menu_identifier
        elif isinstance(menu_identifier, int):
            menu = MasterMenu.objects.filter(menu_id=menu_identifier).first()
        elif isinstance(menu_identifier, str):
            menu = (
                MasterMenu.objects.filter(menu_name__iexact=menu_identifier).first() or
                MasterMenu.objects.filter(url_page__iexact=menu_identifier).first() or
                MasterMenu.objects.filter(menu_name__icontains=menu_identifier).first()
            )
            if not menu and 'teacher' in menu_identifier.lower():
                alt_name = menu_identifier.lower().replace('teacher', 'staff')
                menu = MasterMenu.objects.filter(menu_name__icontains=alt_name).first()
            elif not menu and 'staff' in menu_identifier.lower():
                alt_name = menu_identifier.lower().replace('staff', 'teacher')
                menu = MasterMenu.objects.filter(menu_name__icontains=alt_name).first()

        if not menu:
            menu = resolve_current_menu(request)

        if menu:
            access = RoleAccess.objects.filter(role=user.role, menu=menu).first()
            if access is not None:
                field = f"{action}_access"
                return bool(getattr(access, field, False))

        if parent_fallback:
            p_menu = (
                MasterMenu.objects.filter(menu_name__iexact=parent_fallback).first() or
                MasterMenu.objects.filter(url_page__iexact=parent_fallback).first()
            )
            if p_menu:
                p_access = RoleAccess.objects.filter(role=user.role, menu=p_menu).first()
                if p_access is not None:
                    field = f"{action}_access"
                    return bool(getattr(p_access, field, False))

        # Fallback if no explicit RoleAccess record exists
        if user.role.role_name.lower() == 'superadmin':
            return True
        return False
    except Exception as e:
        print(f"Error checking permission: {e}")
        return False

def sidebar_menu_processor(request):
    if 'user_id' not in request.session:
        return {'sidebar_menus': []}
        
    try:
        from users.models import User, RoleAccess, MasterMenu
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        if not user.role:
            return {'sidebar_menus': []}
        
        # Get all active menus
        all_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
        
        # Check explicit view_access in RoleAccess for this role
        role_access_map = {ra.menu_id: ra.view_access for ra in RoleAccess.objects.filter(role=user.role)}
        
        access_set = set()
        for m in all_menus:
            if m.menu_id in role_access_map:
                if role_access_map[m.menu_id]:
                    access_set.add(m.menu_id)
            else:
                # If no RoleAccess record exists, superadmin gets access by default
                if user.role.role_name.lower() == 'superadmin':
                    access_set.add(m.menu_id)
        
        # Build tree
        def build_tree(parent_id=None):
            tree = []
            for m in all_menus:
                if m.parent_menu_id == parent_id:
                    children = build_tree(m.menu_id)
                    if m.menu_id in access_set or len(children) > 0:
                        m.children = children
                        tree.append(m)
            return tree

        top_menus = build_tree(None)
        return {'sidebar_menus': top_menus}
    except Exception as e:
        print(f"Error in sidebar_menu_processor: {e}")
        return {'sidebar_menus': []}

def user_permissions(request):
    if 'user_id' not in request.session:
        return {'user_perms': {}}
        
    try:
        from users.models import User, RoleAccess, MasterMenu
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        if not user.role:
            return {'user_perms': {}}
            
        accesses = RoleAccess.objects.filter(role=user.role).select_related('menu')
        access_by_menu_id = {ra.menu_id: ra for ra in accesses}
        
        perms = {}
        for menu in MasterMenu.objects.filter(is_active=True):
            if menu.menu_id in access_by_menu_id:
                ra = access_by_menu_id[menu.menu_id]
                p = {
                    'view': ra.view_access,
                    'add': ra.add_access,
                    'edit': ra.edit_access,
                    'delete': ra.delete_access,
                    'export': ra.export_access,
                }
            else:
                # Fallback if no specific row in RoleAccess
                is_sa = bool(user.role.role_name.lower() == 'superadmin')
                p = {
                    'view': is_sa,
                    'add': is_sa,
                    'edit': is_sa,
                    'delete': is_sa,
                    'export': is_sa,
                }
            
            # Key by original Pascal/spaced name, underscores, and lowercase
            key1 = menu.menu_name.replace(' ', '_').replace('&', 'and')
            key2 = menu.menu_name.lower().replace(' ', '_').replace('&', 'and').replace('-', '_')
            perms[key1] = p
            perms[key2] = p
            if 'staff' in key2:
                perms[key2.replace('staff', 'teacher')] = p
            elif 'teacher' in key2:
                perms[key2.replace('teacher', 'staff')] = p
                
        return {'user_perms': perms}
    except Exception as e:
        print(f"Error loading user perms: {e}")
        return {'user_perms': {}}

def current_menu_access_processor(request):
    default_denied = {'view': False, 'add': False, 'edit': False, 'delete': False, 'export': False}
    if 'user_id' not in request.session:
        return {'menu_access': default_denied}
        
    try:
        from users.models import User, RoleAccess
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        if not user.role:
            return {'menu_access': default_denied}
            
        current_menu = resolve_current_menu(request)
        if current_menu:
            access = RoleAccess.objects.filter(role=user.role, menu=current_menu).first()
            if access:
                return {
                    'menu_access': {
                        'view': access.view_access,
                        'add': access.add_access,
                        'edit': access.edit_access,
                        'delete': access.delete_access,
                        'export': access.export_access
                    }
                }
            # Fallback if no specific RoleAccess row exists
            if user.role.role_name.lower() == 'superadmin':
                return {'menu_access': {'view': True, 'add': True, 'edit': True, 'delete': True, 'export': True}}
            return {'menu_access': default_denied}
        else:
            if user.role.role_name.lower() == 'superadmin':
                return {'menu_access': {'view': True, 'add': True, 'edit': True, 'delete': True, 'export': True}}
            return {'menu_access': default_denied}
    except Exception as e:
        print(f"Error in current_menu_access_processor: {e}")
        
    return {'menu_access': default_denied}


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
