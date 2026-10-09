import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
@csrf_exempt
def mobile_students_api(request):
    if request.method == 'GET':
        students = User.objects.filter(role__role_name__iexact='student').values(
            'user_id', 'first_name', 'email', 'phone'
        )
        return JsonResponse({'success': True, 'data': list(students)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_teachers_api(request):
    if request.method == 'GET':
        teachers = User.objects.filter(role__role_name__iexact='teacher').values(
            'user_id', 'first_name', 'email', 'phone'
        )
        return JsonResponse({'success': True, 'data': list(teachers)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
