from users.models import RoleAccess, User

def user_permissions(request):
    if 'user_id' not in request.session:
        return {}
        
    try:
        user = User.objects.select_related('role').get(user_id=request.session['user_id'])
        access_records = RoleAccess.objects.filter(role=user.role, menu__is_active=True).select_related('menu')
        
        perms = {}
        for access in access_records:
            perms[access.menu.menu_name.replace(' & ', '_and_').replace(' ', '_')] = {
                'view': access.view_access,
                'add': access.add_access,
                'edit': access.edit_access,
                'delete': access.delete_access,
                'export': access.export_access
            }
            
        return {'user_perms': perms}
    except User.DoesNotExist:
        return {}
