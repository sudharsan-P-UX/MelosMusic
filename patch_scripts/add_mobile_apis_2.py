import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
from academics.models import Course, Timetable

@csrf_exempt
def mobile_courses_api(request):
    if request.method == 'GET':
        courses = Course.objects.filter(is_active=True).values(
            'course_id', 'course_name', 'description'
        )
        return JsonResponse({'success': True, 'data': list(courses)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_timetable_api(request):
    if request.method == 'GET':
        timetables = Timetable.objects.filter(is_active=True).select_related('course', 'batch', 'teacher').values(
            'timetable_id', 
            'day_of_week', 
            'start_time', 
            'end_time', 
            'course__course_name',
            'batch__batch_name',
            'teacher__first_name'
        )
        return JsonResponse({'success': True, 'data': list(timetables)})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
