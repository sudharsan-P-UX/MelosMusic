import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "path('api/mobile-login/', views.mobile_login_api, name='mobile_login_api'),",
    "path('api/mobile-login/', views.mobile_login_api, name='mobile_login_api'),\n    path('api/mobile-students/', views.mobile_students_api, name='mobile_students_api'),\n    path('api/mobile-teachers/', views.mobile_teachers_api, name='mobile_teachers_api'),"
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
