import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. students_view create
student_add_pattern = r"(password = request\.POST\.get\('password'\)\n\s+)(days_list = request\.POST\.getlist\('days'\))"
student_add_repl = r"""\1confirm_password = request.POST.get('confirm_password')
        if password and password != confirm_password:
            messages.error(request, "Password and confirm password must match.")
            return redirect('students')
        
        \2"""
text = re.sub(student_add_pattern, student_add_repl, text)

# 2. update_student
student_upd_pattern = r"(if password:\n\s+confirm_password = request\.POST\.get\('confirm_password'\)\n\s+)(if password == confirm_password:\n\s+student\.password = password)"
student_upd_repl = r"""\1if password != confirm_password:
                    messages.error(request, "Password and confirm password must match.")
                    return redirect('students')
                student.password = password"""
text = re.sub(student_upd_pattern, student_upd_repl, text)

# 3. teachers_view create
teacher_add_pattern = r"(password = request\.POST\.get\('password'\)\n\s+confirm_password = request\.POST\.get\('confirm_password'\)\n\s+days_list = request\.POST\.getlist\('days'\)\n\s+preferred_days = ', '\.join\(days_list\) if days_list else ''\n\s+# Simple validation\n\s+)(if password != confirm_password:\n\s+pass)"
teacher_add_repl = r"""\1if password and password != confirm_password:
            messages.error(request, "Password and confirm password must match.")
            return redirect('teachers')"""
text = re.sub(teacher_add_pattern, teacher_add_repl, text)

# 4. update_teacher
teacher_upd_pattern = r"(if password:\n\s+confirm_password = request\.POST\.get\('confirm_password'\)\n\s+)(if password == confirm_password:\n\s+teacher\.password = password)"
teacher_upd_repl = r"""\1if password != confirm_password:
                    messages.error(request, "Password and confirm password must match.")
                    return redirect('teachers')
                teacher.password = password"""
text = re.sub(teacher_upd_pattern, teacher_upd_repl, text)

# 5. admin_dashboard_view create user
admin_user_add_pattern = r"(password = request\.POST\.get\('password', ''\)\n\s+role_id = request\.POST\.get\('role_id'\)\n\s+)(try:)"
admin_user_add_repl = r"""\1confirm_password = request.POST.get('confirm_password', '')
            if password and password != confirm_password:
                messages.error(request, "Password and confirm password must match.")
                return redirect('/admin-dashboard/?tab=users')
            
            \2"""
text = re.sub(admin_user_add_pattern, admin_user_add_repl, text)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
