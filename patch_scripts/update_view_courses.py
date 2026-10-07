with open('website/views.py', 'r') as f:
    content = f.read()

new_view = '''
def courses_batches_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    from users.models import User
    user = User.objects.get(user_id=request.session['user_id'])
    
    from academics.models import Course, Batch
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_course':
            Course.objects.create(
                course_code=request.POST.get('course_code'),
                course_name=request.POST.get('course_name'),
                category=request.POST.get('category'),
                duration_months=request.POST.get('duration_months'),
                total_sessions=request.POST.get('total_sessions'),
                fee_amount=request.POST.get('fee_amount'),
                description=request.POST.get('description'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            messages.success(request, 'Course added successfully!')
        elif action == 'add_batch':
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            Batch.objects.create(
                batch_code=request.POST.get('batch_code'),
                batch_name=request.POST.get('batch_name'),
                course_id=course_id,
                teacher_id=teacher_id if teacher_id else None,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                capacity=request.POST.get('capacity'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )
            messages.success(request, 'Batch added successfully!')
        return redirect('courses')
        
    courses = Course.objects.all().order_by('-course_id')
    batches = Batch.objects.all().order_by('-batch_id')
    teachers = User.objects.filter(role__role_name='Teacher', is_active=True)
    
    return render(request, 'website/courses_batches.html', {
        'user': user,
        'page_title': 'Courses & Batches',
        'courses': courses,
        'batches': batches,
        'teachers': teachers
    })
'''

if 'def courses_batches_view' not in content:
    content += '\n' + new_view

with open('website/views.py', 'w') as f:
    f.write(content)
