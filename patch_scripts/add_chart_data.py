import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"(def enrollment_management_view\(request\):.*?)(    return render\(request, 'website/enrollment_management\.html', \{)"

replacement = r"""\1    from django.db.models import Count, Q
    
    # Pie Chart: Enrollments by Course
    course_stats = list(Course.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('course_name', 'enroll_count'))
    
    # Bar Chart: Student Status
    active_students = User.objects.filter(role=student_role, is_active=True).count()
    inactive_students = User.objects.filter(role=student_role, is_active=False).count()
    
    # Horizontal Bar: Batch Capacity
    batch_stats = list(Batch.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('batch_name', 'capacity', 'enroll_count')[:5])
    
\2"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Add to context
context_pattern = r"('students': students,\n\s*'courses': courses,\n\s*'batches': batches,\n\s*'enrollments': enrollments\n\s*\})"
context_replacement = r"""'students': students,
        'courses': courses,
        'batches': batches,
        'enrollments': enrollments,
        'course_stats': course_stats,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'batch_stats': batch_stats
    })"""
content = re.sub(context_pattern, context_replacement, content, flags=re.DOTALL)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
