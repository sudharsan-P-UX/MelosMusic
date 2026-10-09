import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

urls = """
    path('api/mobile-attendance/', views.mobile_attendance_api, name='mobile_attendance_api'),
    path('api/mobile-fees/', views.mobile_fees_api, name='mobile_fees_api'),
    path('api/mobile-users/', views.mobile_users_api, name='mobile_users_api'),
    path('api/mobile-roles/', views.mobile_roles_api, name='mobile_roles_api'),
    path('api/mobile-auditlogs/', views.mobile_auditlogs_api, name='mobile_auditlogs_api'),
"""

text = text.replace(
    "path('api/mobile-menus/', views.mobile_menus_api, name='mobile_menus_api'),",
    "path('api/mobile-menus/', views.mobile_menus_api, name='mobile_menus_api')," + urls
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
