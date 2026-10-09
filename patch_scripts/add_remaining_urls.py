import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

urls = """
    path('api/mobile-events/', views.mobile_events_api, name='mobile_events_api'),
    path('api/mobile-settings/', views.mobile_settings_api, name='mobile_settings_api'),
"""

text = text.replace(
    "path('api/mobile-auditlogs/', views.mobile_auditlogs_api, name='mobile_auditlogs_api'),",
    "path('api/mobile-auditlogs/', views.mobile_auditlogs_api, name='mobile_auditlogs_api')," + urls
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
