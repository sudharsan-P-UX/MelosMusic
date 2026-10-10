import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the generic api exceptions
text = text.replace("'enrollment_date'", "'joining_date'")
text = text.replace("'receipt_number'", "'receipt_no'")

# Add try-except to mobile_dashboard_metrics_api
metrics_fix = """@csrf_exempt
def mobile_dashboard_metrics_api(request):
    try:
        from users.models import User
        from academics.models import Course
        from finance.models import StudentFeeInstallment
        from django.db.models import Sum, F
        
        total_students = User.objects.filter(role__role_name__iexact='student').count()
        active_teachers = User.objects.filter(role__role_name__iexact='teacher').count()
        total_courses = Course.objects.filter(is_active=True).count()
        
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
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})"""

text = re.sub(r'@csrf_exempt\s*def mobile_dashboard_metrics_api.*?return JsonResponse.*?\}\)\n', metrics_fix + '\n', text, flags=re.DOTALL)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
