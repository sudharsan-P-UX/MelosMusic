import re

with open('website/urls.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),",
                    "path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),\n    path('audit-logs/', views.audit_logs_view, name='audit_logs'),")

with open('website/urls.py', 'w', encoding='utf-8') as f:
    f.write(text)
