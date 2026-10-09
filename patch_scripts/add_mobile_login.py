import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_login_code = """
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def mobile_login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uname = data.get('username')
            upass = data.get('password')
            
            user = User.objects.select_related('role').get(first_name=uname, password=upass)
            if user.is_active:
                return JsonResponse({
                    'success': True, 
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'role': user.role.role_name if user.role else 'Student'
                })
            else:
                return JsonResponse({'success': False, 'error': 'Account disabled'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_login_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
