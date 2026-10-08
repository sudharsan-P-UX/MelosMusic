import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Students View patch
old_student_create = """        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        new_student = User.objects.create(
            first_name=fname,
            last_name=lname,
            display_name=name,"""

new_student_create = """        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        user_code = "S1000"
        last_student = User.objects.filter(role=student_role, user_code__startswith='S').order_by('-user_id').first()
        if last_student and last_student.user_code:
            try:
                user_code = f"S{int(last_student.user_code[1:]) + 1}"
            except: pass
            
        new_student = User.objects.create(
            user_code=user_code,
            first_name=fname,
            last_name=lname,
            display_name=name,"""

content = content.replace(old_student_create, new_student_create)

# Teachers View patch
old_teacher_create = """        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        new_teacher = User.objects.create(
            first_name=fname,
            last_name=lname,
            display_name=name,"""

new_teacher_create = """        parts = name.split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        
        user_code = "T2000"
        last_teacher = User.objects.filter(role=teacher_role, user_code__startswith='T').order_by('-user_id').first()
        if last_teacher and last_teacher.user_code:
            try:
                user_code = f"T{int(last_teacher.user_code[1:]) + 1}"
            except: pass
            
        new_teacher = User.objects.create(
            user_code=user_code,
            first_name=fname,
            last_name=lname,
            display_name=name,"""

content = content.replace(old_teacher_create, new_teacher_create)

with open('website/views.py', 'w') as f:
    f.write(content)
