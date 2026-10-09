import re

with open('website/urls.py', 'r') as f:
    content = f.read()

new_url = "    path('attendance-log/', views.attendance_log_view, name='attendance_log'),\n"
content = content.replace("    path('teacher-allocation/', views.teacher_allocation_view, name='teacher_allocation'),\n", 
                          "    path('teacher-allocation/', views.teacher_allocation_view, name='teacher_allocation'),\n" + new_url)

with open('website/urls.py', 'w') as f:
    f.write(content)
