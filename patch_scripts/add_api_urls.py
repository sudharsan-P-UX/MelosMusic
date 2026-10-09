import re

with open('website/urls.py', 'r') as f:
    urls_content = f.read()

if "path('api/get-student/'" not in urls_content:
    urls_content = urls_content.replace(
        "path('student-allocation/', views.student_allocation_view, name='student_allocation'),",
        "path('student-allocation/', views.student_allocation_view, name='student_allocation'),\n    path('api/get-student/', views.api_get_student_details, name='api_get_student'),\n    path('api/get-batch/', views.api_get_batch_details, name='api_get_batch'),"
    )
    with open('website/urls.py', 'w') as f:
        f.write(urls_content)
