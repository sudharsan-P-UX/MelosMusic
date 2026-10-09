import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_context = """    return render(request, 'website/student_course.html', {
        'user': user,
        'page_title': 'Allocation Details',
        'enrollments': enrollments,
        'courses': courses
    })"""

new_context = """    
    # Role based filtering
    if user.role and user.role.role_name == 'Student':
        enrollments = enrollments.filter(student=user)
        
    return render(request, 'website/student_course.html', {
        'user': user,
        'page_title': 'Allocation Details',
        'allocations': enrollments,  # Changed to allocations to match template
        'courses': courses
    })"""

content = content.replace(old_context, new_context)

with open('website/views.py', 'w') as f:
    f.write(content)
