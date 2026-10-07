with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('fees/reports/'," not in content:
    content = content.replace("path('fees/refunds/', views.refunds_view, name='refunds'),", "path('fees/refunds/', views.refunds_view, name='refunds'),\n    path('fees/reports/', views.reports_view, name='reports'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
