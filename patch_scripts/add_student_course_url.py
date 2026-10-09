import re

with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('student-course/'" not in content:
    content = content.replace(
        "path('students/', views.students_view, name='students'),",
        "path('students/', views.students_view, name='students'),\n    path('student-course/', views.student_course_view, name='student_course'),"
    )
    with open('website/urls.py', 'w') as f:
        f.write(content)
