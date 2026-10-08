import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_create = """            try:
                role = Role.objects.get(role_id=role_id)
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role
                )"""

new_create = """            try:
                role = Role.objects.get(role_id=role_id)
                
                # Auto-generate user_code for Students and Teachers
                user_code = None
                if role.role_name.lower() == 'student':
                    last_student = User.objects.filter(role=role, user_code__startswith='S').order_by('-user_id').first()
                    if last_student and last_student.user_code:
                        try:
                            last_num = int(last_student.user_code[1:])
                            user_code = f"S{last_num + 1}"
                        except:
                            user_code = "S1000"
                    else:
                        user_code = "S1000"
                elif role.role_name.lower() == 'teacher':
                    last_teacher = User.objects.filter(role=role, user_code__startswith='T').order_by('-user_id').first()
                    if last_teacher and last_teacher.user_code:
                        try:
                            last_num = int(last_teacher.user_code[1:])
                            user_code = f"T{last_num + 1}"
                        except:
                            user_code = "T2000"
                    else:
                        user_code = "T2000"
                        
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role,
                    user_code=user_code
                )"""

content = content.replace(old_create, new_create)

with open('website/views.py', 'w') as f:
    f.write(content)
