with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('fees/collection/'," not in content:
    content = content.replace("path('fees/dashboard/', views.fee_dashboard_view, name='fee_dashboard'),", "path('fees/dashboard/', views.fee_dashboard_view, name='fee_dashboard'),\n    path('fees/collection/', views.fee_collection_view, name='fee_collection'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
