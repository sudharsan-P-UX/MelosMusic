with open('website/urls.py', 'r') as f:
    content = f.read()

import re
content = re.sub(
    r"path\('page/<str:page_name>/', views.generic_page, name='generic_page'\),",
    r"path('enrollment_management/', views.enrollment_management_view, name='enrollment_management'),\n    path('page/<str:page_name>/', views.generic_page, name='generic_page'),",
    content
)

with open('website/urls.py', 'w') as f:
    f.write(content)
