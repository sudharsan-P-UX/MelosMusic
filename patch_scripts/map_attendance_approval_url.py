import re

with open('website/urls.py', 'r') as f:
    content = f.read()

new_url = "    path('attendance-approval/', views.attendance_approval_view, name='attendance_approval'),\n"
content = content.replace("    path('attendance-log/', views.attendance_log_view, name='attendance_log'),\n", 
                          "    path('attendance-log/', views.attendance_log_view, name='attendance_log'),\n" + new_url)

with open('website/urls.py', 'w') as f:
    f.write(content)
