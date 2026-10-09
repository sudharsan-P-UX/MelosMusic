with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad_view = """    enrollments = StudentEnrollment.objects.all()
    
    return render(request, 'website/enrollment_management.html', {"""

good_view = """    enrollments = StudentEnrollment.objects.all()
    
    from django.db.models import Count, Q
    
    course_stats = list(Course.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('course_name', 'enroll_count'))
    
    active_students = User.objects.filter(role=student_role, is_active=True).count()
    inactive_students = User.objects.filter(role=student_role, is_active=False).count()
    
    batch_stats = list(Batch.objects.annotate(
        enroll_count=Count('studentenrollment', filter=Q(studentenrollment__status=1))
    ).values('batch_name', 'capacity', 'enroll_count')[:5])
    
    return render(request, 'website/enrollment_management.html', {
        'course_stats': course_stats,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'batch_stats': batch_stats,"""

text = text.replace(bad_view, good_view)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
