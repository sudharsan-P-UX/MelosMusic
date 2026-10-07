with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """def enrollment_management_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Course, Batch, StudentEnrollment
    from users.models import Role, RoleGroup
    
    rg, _ = RoleGroup.objects.get_or_create(role_group_name="Students")
    student_role, _ = Role.objects.get_or_create(role_name="Student", defaults={'role_group': rg})
    
    students = User.objects.filter(role=student_role, is_active=True)
    courses = Course.objects.all()
    batches = Batch.objects.all()
    enrollments = StudentEnrollment.objects.all()
    
    return render(request, 'website/enrollment_management.html', {
        'user': user,
        'page_title': 'Enrollment Management',
        'students': students,
        'courses': courses,
        'batches': batches,
        'enrollments': enrollments
    })

def generic_page"""

content = content.replace('def generic_page', new_view)

with open('website/views.py', 'w') as f:
    f.write(content)
