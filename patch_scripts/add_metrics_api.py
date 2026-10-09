import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
from django.db.models import Sum, F

@csrf_exempt
def mobile_dashboard_metrics_api(request):
    if request.method == 'GET':
        total_students = User.objects.filter(role__role_name__iexact='student').count()
        active_teachers = User.objects.filter(role__role_name__iexact='teacher').count()
        total_courses = Course.objects.filter(is_active=True).count()
        
        from finance.models import StudentFeeInstallment
        pending_fees = StudentFeeInstallment.objects.filter(amount__gt=F('paid_amount')).aggregate(
            total_pending=Sum(F('amount') - F('paid_amount'))
        )['total_pending'] or 0
        
        metrics = [
            {'title': 'Total Students', 'value': str(total_students), 'icon': 'people', 'color': 'blue'},
            {'title': 'Active Teachers', 'value': str(active_teachers), 'icon': 'school', 'color': 'orange'},
            {'title': 'Active Courses', 'value': str(total_courses), 'icon': 'music_note', 'color': 'purple'},
            {'title': 'Pending Fees', 'value': f'${pending_fees}', 'icon': 'money', 'color': 'red'},
        ]
        return JsonResponse({'success': True, 'data': metrics})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
