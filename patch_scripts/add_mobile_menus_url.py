import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "path('api/mobile-timetable/', views.mobile_timetable_api, name='mobile_timetable_api'),",
    "path('api/mobile-timetable/', views.mobile_timetable_api, name='mobile_timetable_api'),\n    path('api/mobile-menus/', views.mobile_menus_api, name='mobile_menus_api'),"
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
