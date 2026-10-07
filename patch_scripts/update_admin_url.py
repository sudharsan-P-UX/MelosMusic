import re

with open('website/urls.py', 'r') as f:
    content = f.read()

if "path('admin-dashboard/'," not in content:
    old_urlpatterns = "urlpatterns = ["
    new_urlpatterns = "urlpatterns = [\n    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),"
    content = content.replace(old_urlpatterns, new_urlpatterns)

with open('website/urls.py', 'w') as f:
    f.write(content)
