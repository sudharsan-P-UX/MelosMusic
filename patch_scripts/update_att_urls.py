with open('website/urls.py', 'r') as f:
    content = f.read()

new_urls = """    path('attendance/student/', views.student_attendance_view, name='student_attendance'),
    path('attendance/teacher/', views.teacher_attendance_view, name='teacher_attendance'),
"""
if 'attendance/student/' not in content:
    content = content.replace("path('timetable/', views.timetable_view, name='timetable'),", "path('timetable/', views.timetable_view, name='timetable'),\n" + new_urls)

with open('website/urls.py', 'w') as f:
    f.write(content)
