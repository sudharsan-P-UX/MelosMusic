import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User, Role

student_role = Role.objects.filter(role_name__iexact='student').first()
teacher_role = Role.objects.filter(role_name__iexact='teacher').first()

if student_role:
    students = User.objects.filter(role=student_role).order_by('user_id')
    last_id = 1000
    for s in students:
        if not s.user_code:
            s.user_code = f"S{last_id}"
            s.save()
            print(f"Fixed student {s.display_name} -> {s.user_code}")
        else:
            try:
                last_id = int(s.user_code[1:]) + 1
            except: pass

if teacher_role:
    teachers = User.objects.filter(role=teacher_role).order_by('user_id')
    last_id = 2000
    for t in teachers:
        if not t.user_code:
            t.user_code = f"T{last_id}"
            t.save()
            print(f"Fixed teacher {t.display_name} -> {t.user_code}")
        else:
            try:
                last_id = int(t.user_code[1:]) + 1
            except: pass
