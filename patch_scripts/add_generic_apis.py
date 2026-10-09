import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
from finance.models import StudentFee
from academics.models import StudentAttendance

@csrf_exempt
def mobile_attendance_api(request):
    if request.method == 'GET':
        records = StudentAttendance.objects.all().select_related('student', 'course').values(
            'date', 'student__first_name', 'course__course_name', 'status'
        )[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_fees_api(request):
    if request.method == 'GET':
        records = StudentFee.objects.all().select_related('student').values(
            'student__first_name', 'total_fee_amount', 'fee_status', 'due_date'
        )[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_users_api(request):
    if request.method == 'GET':
        records = User.objects.all().select_related('role').values(
            'first_name', 'email', 'role__role_name', 'is_active'
        )[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_roles_api(request):
    if request.method == 'GET':
        from users.models import Role
        records = Role.objects.all().values('role_name', 'is_active')
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_auditlogs_api(request):
    if request.method == 'GET':
        from users.models import AuditLog
        records = AuditLog.objects.all().select_related('user').values(
            'user__first_name', 'action', 'table_name', 'action_date'
        ).order_by('-action_date')[:50]
        return JsonResponse({'success': True, 'data': list(records)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
