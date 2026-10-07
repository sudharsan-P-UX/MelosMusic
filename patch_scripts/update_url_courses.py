with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('courses/'," not in content:
    content = content.replace("path('timetable/', views.timetable_view, name='timetable'),", "path('timetable/', views.timetable_view, name='timetable'),\n    path('courses/', views.courses_batches_view, name='courses'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
