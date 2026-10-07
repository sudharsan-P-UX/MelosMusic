with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('fees/dashboard/'," not in content:
    content = content.replace("path('timetable/', views.timetable_view, name='timetable'),", "path('timetable/', views.timetable_view, name='timetable'),\n    path('fees/dashboard/', views.fee_dashboard_view, name='fee_dashboard'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
