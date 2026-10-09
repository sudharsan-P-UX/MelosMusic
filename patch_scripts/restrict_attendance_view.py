import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Fix student_attendance_view
old_student_view_filters = """    details = LeaveRequest.objects.filter(user_type='Student').select_related('user').order_by('-applied_date')
    
    if selected_student:
        details = details.filter(user_id=selected_student)"""

new_student_view_filters = """    details = LeaveRequest.objects.filter(user_type='Student').select_related('user').order_by('-applied_date')
    
    if user.role.role_name == 'Student':
        details = details.filter(user=user)
        selected_student = str(user.user_id)
    elif selected_student:
        details = details.filter(user_id=selected_student)"""

content = content.replace(old_student_view_filters, new_student_view_filters)

# Fix teacher_attendance_view
old_teacher_view_filters = """    details = LeaveRequest.objects.filter(user_type='Teacher').select_related('user').order_by('-applied_date')
    
    if selected_teacher:
        details = details.filter(user_id=selected_teacher)"""

new_teacher_view_filters = """    details = LeaveRequest.objects.filter(user_type='Teacher').select_related('user').order_by('-applied_date')
    
    if user.role.role_name == 'Teacher':
        details = details.filter(user=user)
        selected_teacher = str(user.user_id)
    elif selected_teacher:
        details = details.filter(user_id=selected_teacher)"""

content = content.replace(old_teacher_view_filters, new_teacher_view_filters)

with open('website/views.py', 'w') as f:
    f.write(content)
