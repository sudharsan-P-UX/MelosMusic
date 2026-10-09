import re

with open('website/views.py', 'r') as f:
    content = f.read()

# student_attendance_view
old_student_post = """    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        batch_id = request.POST.get('batch_id')"""

new_student_post = """    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            from academics.models import LeaveRequest
            student_id = request.POST.get('student_id')
            student = User.objects.get(user_id=student_id)
            LeaveRequest.objects.create(
                user=student,
                user_type='Student',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days'),
                request_type=request.POST.get('request_type'),
                created_by=user.user_id
            )
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('student_attendance')
            
        attendance_date = request.POST.get('attendance_date')
        batch_id = request.POST.get('batch_id')"""

content = content.replace(old_student_post, new_student_post)

# teacher_attendance_view
old_teacher_post = """    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        teacher_id = request.POST.get('teacher_id')"""
        
new_teacher_post = """    if request.method == 'POST':
        if request.POST.get('action') == 'apply_leave':
            from academics.models import LeaveRequest
            teacher_id = request.POST.get('teacher_id')
            teacher = User.objects.get(user_id=teacher_id)
            LeaveRequest.objects.create(
                user=teacher,
                user_type='Teacher',
                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days'),
                request_type=request.POST.get('request_type'),
                created_by=user.user_id
            )
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('teacher_attendance')
            
        attendance_date = request.POST.get('attendance_date')
        teacher_id = request.POST.get('teacher_id')"""

content = content.replace(old_teacher_post, new_teacher_post)

with open('website/views.py', 'w') as f:
    f.write(content)
