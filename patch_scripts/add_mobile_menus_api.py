import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
from users.models import MasterMenu, RoleAccess

@csrf_exempt
def mobile_menus_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = User.objects.select_related('role').get(user_id=user_id)
            
            # Get all active menus
            all_menus = list(MasterMenu.objects.filter(is_active=True).order_by('display_order', 'menu_id'))
            
            # Get role access
            access_records = RoleAccess.objects.filter(role=user.role, view_access=True).values_list('menu_id', flat=True)
            access_set = set(access_records)
            
            # We will flatten the menu structure for the mobile grid, or return a list of accessible menus.
            # For simplicity in mobile, let's just return all accessible menus that are NOT parent containers 
            # (i.e. they actually have a url_page), OR we just return all accessible menus.
            mobile_menus = []
            for m in all_menus:
                if m.menu_id in access_set and m.url_page and m.url_page != '#':
                    mobile_menus.append({
                        'menu_id': m.menu_id,
                        'menu_name': m.menu_name,
                        'url_page': m.url_page,
                        'parent_menu_id': m.parent_menu_id
                    })
                    
            return JsonResponse({'success': True, 'data': mobile_menus})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
