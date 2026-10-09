import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("path('api/get-student/', views.api_get_student_details, name='api_get_student'),", 
                    "path('api/get-student/', views.api_get_student_details, name='api_get_student'),\n    path('api/mobile-login/', views.mobile_login_api, name='mobile_login_api'),")

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
