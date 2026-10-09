import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Patch students_view
student_add_pattern = r"(\s*)(new_student = User\.objects\.create\()"
student_add_check = r"""\1# Uniqueness checks
\1if User.objects.filter(first_name__iexact=fname).exists():
\1    messages.error(request, "Username (First Name) already exists.")
\1    return redirect('students')
\1if User.objects.filter(email__iexact=email).exists():
\1    messages.error(request, "Email already exists.")
\1    return redirect('students')
\1if User.objects.filter(phone=phone).exists():
\1    messages.error(request, "Phone already exists.")
\1    return redirect('students')
\1\2"""
content = re.sub(student_add_pattern, student_add_check, content, count=1)

# 2. Patch update_student
student_upd_pattern = r"(\s*)(student\.first_name = parts\[0\])"
student_upd_check = r"""\1fname = parts[0]
\1email = request.POST.get('email')
\1phone = request.POST.get('phone')
\1if User.objects.filter(first_name__iexact=fname).exclude(user_id=student_id).exists():
\1    messages.error(request, "Username (First Name) already exists.")
\1    return redirect('students')
\1if User.objects.filter(email__iexact=email).exclude(user_id=student_id).exists():
\1    messages.error(request, "Email already exists.")
\1    return redirect('students')
\1if User.objects.filter(phone=phone).exclude(user_id=student_id).exists():
\1    messages.error(request, "Phone already exists.")
\1    return redirect('students')
\1\2"""
content = re.sub(student_upd_pattern, student_upd_check, content, count=1)

# 3. Patch teachers_view
teacher_add_pattern = r"(\s*)(new_teacher = User\.objects\.create\()"
teacher_add_check = r"""\1# Uniqueness checks
\1if User.objects.filter(first_name__iexact=fname).exists():
\1    messages.error(request, "Username (First Name) already exists.")
\1    return redirect('teachers')
\1if User.objects.filter(email__iexact=email).exists():
\1    messages.error(request, "Email already exists.")
\1    return redirect('teachers')
\1if User.objects.filter(phone=phone).exists():
\1    messages.error(request, "Phone already exists.")
\1    return redirect('teachers')
\1\2"""
content = re.sub(teacher_add_pattern, teacher_add_check, content, count=1)

# 4. Patch update_teacher
teacher_upd_pattern = r"(\s*)(teacher\.first_name = parts\[0\])"
teacher_upd_check = r"""\1fname = parts[0]
\1email = request.POST.get('email')
\1phone = request.POST.get('phone')
\1if User.objects.filter(first_name__iexact=fname).exclude(user_id=teacher_id).exists():
\1    messages.error(request, "Username (First Name) already exists.")
\1    return redirect('teachers')
\1if User.objects.filter(email__iexact=email).exclude(user_id=teacher_id).exists():
\1    messages.error(request, "Email already exists.")
\1    return redirect('teachers')
\1if User.objects.filter(phone=phone).exclude(user_id=teacher_id).exists():
\1    messages.error(request, "Phone already exists.")
\1    return redirect('teachers')
\1\2"""
content = re.sub(teacher_upd_pattern, teacher_upd_check, content, count=1)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
