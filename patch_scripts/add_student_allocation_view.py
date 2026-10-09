import re

with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """
def student_allocation_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Course, StudentEnrollment, Batch
    from django.db.models import Q
    from django.http import JsonResponse
    import json
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'allocate_student':
            student_id = request.POST.get('student_id')
            batch_id = request.POST.get('batch_id')
            
            try:
                student = User.objects.get(user_id=student_id)
                batch = Batch.objects.get(batch_id=batch_id)
                
                # Check if already enrolled in this course
                existing = StudentEnrollment.objects.filter(student=student, course=batch.course).first()
                if existing:
                    existing.batch = batch
                    existing.save()
                    messages.success(request, 'Student allocation updated successfully.')
                else:
                    StudentEnrollment.objects.create(
                        student=student,
                        course=batch.course,
                        batch=batch,
                        joining_date=batch.start_date,
                        status=1
                    )
                    messages.success(request, 'Student allocated successfully.')
            except Exception as e:
                messages.error(request, f'Error allocating student: {str(e)}')
            return redirect('student_allocation')
            
    # GET Request
    allocations = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')
    
    # Pre-fetch for the modal dropdowns
    students = User.objects.filter(role__role_name='Student', is_active=True).order_by('display_name')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True).order_by('display_name')
    batches = Batch.objects.select_related('course', 'teacher').filter(is_active=True).order_by('batch_name')
    
    # Calculate remaining capacity for batches
    for batch in batches:
        enrolled_count = StudentEnrollment.objects.filter(batch=batch, status=1).count()
        batch.remaining_capacity = (batch.capacity or 0) - enrolled_count
    
    return render(request, 'website/student_allocation.html', {
        'user': user,
        'page_title': 'Student Course Allocation',
        'allocations': allocations,
        'students': students,
        'teachers': teachers,
        'batches': batches,
    })

def api_get_student_details(request):
    user_id = request.GET.get('id')
    try:
        student = User.objects.get(user_id=user_id)
        return JsonResponse({
            'success': True,
            'student_code': student.user_code,
            'name': student.display_name,
            'phone': student.mobile_number
        })
    except:
        return JsonResponse({'success': False})

def api_get_batch_details(request):
    batch_id = request.GET.get('id')
    try:
        from academics.models import Batch, StudentEnrollment
        batch = Batch.objects.get(batch_id=batch_id)
        enrolled_count = StudentEnrollment.objects.filter(batch=batch, status=1).count()
        remaining = (batch.capacity or 0) - enrolled_count
        
        return JsonResponse({
            'success': True,
            'course_id': batch.course.course_id,
            'course_name': batch.course.course_name,
            'batch_code': batch.batch_code,
            'batch_name': batch.batch_name,
            'teacher_id': batch.teacher.user_id if batch.teacher else '',
            'teacher_name': batch.teacher.display_name if batch.teacher else '',
            'teacher_phone': batch.teacher.mobile_number if batch.teacher else '',
            'start_time': batch.start_time.strftime('%H:%M') if batch.start_time else '',
            'end_time': batch.end_time.strftime('%H:%M') if batch.end_time else '',
            'remaining_capacity': remaining
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
"""

if "def student_allocation_view" not in content:
    with open('website/views.py', 'a') as f:
        f.write(new_view)
