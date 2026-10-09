import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

urls = """
    path('api/mobile-generic/', views.mobile_generic_api, name='mobile_generic_api'),
"""

text = text.replace(
    "path('api/mobile-settings/', views.mobile_settings_api, name='mobile_settings_api'),",
    "path('api/mobile-settings/', views.mobile_settings_api, name='mobile_settings_api')," + urls
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
