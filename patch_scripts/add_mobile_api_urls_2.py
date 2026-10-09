import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "path('api/mobile-teachers/', views.mobile_teachers_api, name='mobile_teachers_api'),",
    "path('api/mobile-teachers/', views.mobile_teachers_api, name='mobile_teachers_api'),\n    path('api/mobile-courses/', views.mobile_courses_api, name='mobile_courses_api'),\n    path('api/mobile-timetable/', views.mobile_timetable_api, name='mobile_timetable_api'),"
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
