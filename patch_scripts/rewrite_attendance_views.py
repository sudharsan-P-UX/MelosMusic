import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Replace student_attendance_view
old_student_view = re.search(r"def student_attendance_view\(request\):.*?return render\(request, 'website/student_attendance\.html', \{.*?\n    \}\)", content, re.DOTALL).group(0)

new_student_view = """def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    from users.models import User
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Batch, LeaveRequest
    
    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            student_id = request.POST.get('student_id')
            student = User.objects.get(user_id=student_id)
            LeaveRequest.objects.create(
                user=student,
                user_type='Student',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),
                created_by=user.user_id
            )
            messages.success(request, 'Attendance request submitted successfully!')
            return redirect('student_attendance')
            
    # Filters
    selected_batch = request.GET.get('batch_id', '')
    selected_student = request.GET.get('student_id', '')
    selected_date = request.GET.get('date', '')
    
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name__iexact='student', is_active=True)
    
    details = LeaveRequest.objects.filter(user_type='Student').select_related('user').order_by('-applied_date')
    
    if selected_student:
        details = details.filter(user_id=selected_student)
        
    if selected_date:
        details = details.filter(from_date__lte=selected_date, to_date__gte=selected_date)

    return render(request, 'website/student_attendance.html', {
        'user': user,
        'page_title': 'Student Attendance',
        'batches': batches,
        'students': students,
        'details': details,
        'selected_batch': selected_batch,
        'selected_student': selected_student,
        'selected_date': selected_date
    })"""

content = content.replace(old_student_view, new_student_view)

# Replace teacher_attendance_view
old_teacher_view = re.search(r"def teacher_attendance_view\(request\):.*?return render\(request, 'website/teacher_attendance\.html', \{.*?\n    \}\)", content, re.DOTALL).group(0)

new_teacher_view = """def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    from users.models import User
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import LeaveRequest
    
    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            teacher_id = request.POST.get('teacher_id')
            teacher = User.objects.get(user_id=teacher_id)
            LeaveRequest.objects.create(
                user=teacher,
                user_type='Teacher',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),
                created_by=user.user_id
            )
            messages.success(request, 'Attendance request submitted successfully!')
            return redirect('teacher_attendance')
            
    # Filters
    selected_teacher = request.GET.get('teacher_id', '')
    selected_date = request.GET.get('date', '')
    
    teachers = User.objects.filter(role__role_name__iexact='teacher', is_active=True)
    
    details = LeaveRequest.objects.filter(user_type='Teacher').select_related('user').order_by('-applied_date')
    
    if selected_teacher:
        details = details.filter(user_id=selected_teacher)
        
    if selected_date:
        details = details.filter(from_date__lte=selected_date, to_date__gte=selected_date)

    return render(request, 'website/teacher_attendance.html', {
        'user': user,
        'page_title': 'Teacher Attendance',
        'teachers': teachers,
        'details': details,
        'selected_teacher': selected_teacher,
        'selected_date': selected_date
    })"""

content = content.replace(old_teacher_view, new_teacher_view)

with open('website/views.py', 'w') as f:
    f.write(content)
