with open('website/urls.py', 'r') as f:
    content = f.read()

content = content.replace("path('page/<str:page_name>/', views.generic_page, name='generic_page'),", "path('timetable/', views.timetable_view, name='timetable'),\n    path('page/<str:page_name>/', views.generic_page, name='generic_page'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
