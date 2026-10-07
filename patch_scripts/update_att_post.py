with open('website/views.py', 'r') as f:
    content = f.read()

# Replace student_attendance_view
old_student = '''def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Batch, StudentAttendanceDetail
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name='Student', is_active=True)
    
    # Just grab all details for now to mock the table
    details = StudentAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/student_attendance.html', {'''

new_student = '''def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Batch, StudentAttendance, StudentAttendanceDetail
    
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        batch_id = request.POST.get('batch_id')
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        batch = Batch.objects.get(batch_id=batch_id)
        student = User.objects.get(user_id=student_id)
        
        # Get or create the Master record for this day and batch
        master, created = StudentAttendance.objects.get_or_create(
            attendance_date=attendance_date,
            batch=batch,
            defaults={'created_by': user.user_id, 'course': batch.course}
        )
        
        # Create the detail record
        StudentAttendanceDetail.objects.create(
            student_attendance=master,
            student=student,
            attendance_status=int(status),
            remarks=remarks,
            created_by=user.user_id
        )
        messages.success(request, 'Student attendance recorded successfully!')
        return redirect('student_attendance')
        
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name='Student', is_active=True)
    
    details = StudentAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/student_attendance.html', {'''
content = content.replace(old_student, new_student)

# Replace teacher_attendance_view
old_teacher = '''def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import TeacherAttendanceDetail
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    details = TeacherAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/teacher_attendance.html', {'''

new_teacher = '''def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import TeacherAttendance, TeacherAttendanceDetail
    
    if request.method == 'POST':
        attendance_date = request.POST.get('attendance_date')
        teacher_id = request.POST.get('teacher_id')
        status = request.POST.get('status')
        check_in = request.POST.get('check_in_time')
        check_out = request.POST.get('check_out_time')
        remarks = request.POST.get('remarks')
        
        teacher = User.objects.get(user_id=teacher_id)
        
        master, created = TeacherAttendance.objects.get_or_create(
            attendance_date=attendance_date,
            defaults={'created_by': user.user_id}
        )
        
        TeacherAttendanceDetail.objects.create(
            teacher_attendance=master,
            teacher=teacher,
            attendance_status=int(status),
            check_in_time=check_in if check_in else None,
            check_out_time=check_out if check_out else None,
            remarks=remarks,
            created_by=user.user_id
        )
        messages.success(request, 'Teacher attendance recorded successfully!')
        return redirect('teacher_attendance')
        
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    details = TeacherAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/teacher_attendance.html', {'''
content = content.replace(old_teacher, new_teacher)

with open('website/views.py', 'w') as f:
    f.write(content)
