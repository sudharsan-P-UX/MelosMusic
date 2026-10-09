import re

with open('website/views.py', 'r') as f:
    content = f.read()

# I will append the view at the end of the file
new_view = """
def student_course_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    from academics.models import Course, StudentEnrollment
    from django.db.models import Q
    
    enrollments = StudentEnrollment.objects.all().order_by('-created_date')
    courses = Course.objects.filter(is_active=True)
    
    # Filter logic
    search = request.GET.get('search', '')
    course_id = request.GET.get('course_id', '')
    
    if search:
        enrollments = enrollments.filter(
            Q(student__display_name__icontains=search) | 
            Q(student__user_code__icontains=search) | 
            Q(course__course_name__icontains=search)
        )
        
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
        
    return render(request, 'website/student_course.html', {
        'user': user,
        'page_title': 'Student Course',
        'enrollments': enrollments,
        'courses': courses
    })
"""

if "def student_course_view" not in content:
    with open('website/views.py', 'a') as f:
        f.write(new_view)
