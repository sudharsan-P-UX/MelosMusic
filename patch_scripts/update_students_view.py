with open('website/views.py', 'r') as f:
    content = f.read()

import re

old_view_regex = r'def students_view\(request\):.*?return render\(request, \'website/students\.html\', \{.*?\}\)'

new_view = """def students_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Course, Batch, StudentEnrollment
    from users.models import Role, RoleGroup
    
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Students")
    student_role, _ = Role.objects.get_or_create(role_name="Student", defaults={'role_group': rg})
    
    if request.method == 'POST':
        name = request.POST.get('student_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        parent_name = request.POST.get('parent_name')
        parent_phone = request.POST.get('parent_phone')
        
        course_id = request.POST.get('course_id')
        batch_id = request.POST.get('batch_id')
        joining_date = request.POST.get('joining_date')
        
        status = request.POST.get('status') == '1'
        password = request.POST.get('password')
        
        days_list = request.POST.getlist('days')
        preferred_days = ', '.join(days_list) if days_list else request.POST.get('days', '')
        
        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        new_student = User.objects.create(
            first_name=fname,
            last_name=lname,
            display_name=name,
            email=email,
            phone=phone,
            gender=gender,
            dob=dob if dob else None,
            address=address,
            parent_name=parent_name,
            parent_phone=parent_phone,
            is_active=status,
            role=student_role,
            password=password,
            preferred_days=preferred_days
        )
        
        if course_id:
            course = Course.objects.get(course_id=course_id)
            batch = Batch.objects.get(batch_id=batch_id) if batch_id else None
            StudentEnrollment.objects.create(
                student=new_student,
                course=course,
                batch=batch,
                joining_date=joining_date if joining_date else None,
                status=1 if status else 0
            )
            
        messages.success(request, 'Student added successfully!')
        return redirect('students')
        
    students = User.objects.filter(role=student_role).order_by('-user_id')
        
    return render(request, 'website/students.html', {
        'user': user,
        'courses': courses,
        'batches': batches,
        'students': students,
        'page_title': 'Student Profile'
    })"""

content = re.sub(old_view_regex, new_view, content, flags=re.DOTALL)

with open('website/views.py', 'w') as f:
    f.write(content)
