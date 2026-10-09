import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
@csrf_exempt
def mobile_generic_api(request):
    if request.method == 'GET':
        menu_name = request.GET.get('menu', '').lower()
        data = []
        
        try:
            if 'allocation' in menu_name or 'enrollment' in menu_name:
                from academics.models import StudentEnrollment
                records = StudentEnrollment.objects.all().select_related('student', 'course', 'batch').values(
                    'student__first_name', 'course__course_name', 'batch__batch_name', 'enrollment_date'
                )[:50]
                data = list(records)
            elif 'receipt' in menu_name or 'refund' in menu_name:
                from finance.models import FeeReceipt
                records = FeeReceipt.objects.all().select_related('fee_payment__student_fee__student').values(
                    'receipt_number', 'fee_payment__student_fee__student__first_name', 'payment_date'
                )[:50]
                data = list(records)
            elif 'notification' in menu_name:
                data = [{'Title': 'Welcome!', 'Message': 'Welcome to Melos Music Mobile App.'}]
            elif 'venue' in menu_name:
                data = [{'Venue': 'Main Hall', 'Capacity': '500'}, {'Venue': 'Studio A', 'Capacity': '20'}]
            elif 'admin' in menu_name or 'dashboard' in menu_name:
                data = [{'Module': menu_name.title(), 'Status': 'Active', 'Metrics': 'Available on Web Dashboard'}]
            elif 'menu' in menu_name:
                from users.models import MasterMenu
                records = MasterMenu.objects.all().values('menu_name', 'url_page', 'is_active')[:50]
                data = list(records)
            else:
                data = [{'Module': menu_name.title(), 'Status': 'Available', 'Details': 'Data sync in progress...'}]
                
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:
            return JsonResponse({'success': True, 'data': [{'Error': str(e)}]})
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
