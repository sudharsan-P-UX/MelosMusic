with open('website/urls.py', 'r') as f:
    content = f.read()

import re

# Add path for events
content = re.sub(
    r"path\('enrollment_management/', views.enrollment_management_view, name='enrollment_management'\),",
    r"path('enrollment_management/', views.enrollment_management_view, name='enrollment_management'),\n    path('events/', views.events_dashboard_view, name='events_dashboard'),",
    content
)

with open('website/urls.py', 'w') as f:
    f.write(content)
