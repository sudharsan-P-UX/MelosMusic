with open('website/views.py', 'r') as f:
    content = f.read()

new_views = '''
def student_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Batch, StudentAttendanceDetail
    batches = Batch.objects.filter(is_active=True)
    students = User.objects.filter(role__role_name='Student', is_active=True)
    
    # Just grab all details for now to mock the table
    details = StudentAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/student_attendance.html', {
        'user': user,
        'page_title': 'Student Attendance',
        'batches': batches,
        'students': students,
        'details': details
    })

def teacher_attendance_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import TeacherAttendanceDetail
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    details = TeacherAttendanceDetail.objects.all().order_by('-created_date')
    
    return render(request, 'website/teacher_attendance.html', {
        'user': user,
        'page_title': 'Teacher Attendance',
        'teachers': teachers,
        'details': details
    })
'''

if 'def student_attendance_view' not in content:
    content += '\n' + new_views

with open('website/views.py', 'w') as f:
    f.write(content)
