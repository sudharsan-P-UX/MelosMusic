import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User, Role

student_role = Role.objects.filter(role_name__iexact='student').first()
teacher_role = Role.objects.filter(role_name__iexact='teacher').first()

if student_role:
    students = User.objects.filter(role=student_role).order_by('user_id')
    for idx, s in enumerate(students):
        s.user_code = f"S{1000 + idx}"
        s.save()
    print(f"Updated {students.count()} students")

if teacher_role:
    teachers = User.objects.filter(role=teacher_role).order_by('user_id')
    for idx, t in enumerate(teachers):
        t.user_code = f"T{2000 + idx}"
        t.save()
    print(f"Updated {teachers.count()} teachers")
