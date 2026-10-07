import re

with open('website/urls.py', 'r') as f:
    content = f.read()

content = content.replace("path('events/', views.events_dashboard_view, name='events_dashboard'),",
"path('events/', views.events_dashboard_view, name='events_dashboard'),\n    path('events/create/', views.create_event_view, name='create_event'),")

with open('website/urls.py', 'w') as f:
    f.write(content)
