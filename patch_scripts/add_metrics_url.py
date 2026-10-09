import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

urls = """
    path('api/mobile-dashboard-metrics/', views.mobile_dashboard_metrics_api, name='mobile_dashboard_metrics_api'),
"""

text = text.replace(
    "path('api/mobile-generic/', views.mobile_generic_api, name='mobile_generic_api'),",
    "path('api/mobile-generic/', views.mobile_generic_api, name='mobile_generic_api')," + urls
)

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
