import re

with open('website/views.py', 'r') as f:
    content = f.read()

content = content.replace(
    'def api_get_teacher_details(request):',
    'from django.http import JsonResponse\ndef api_get_teacher_details(request):'
)

with open('website/views.py', 'w') as f:
    f.write(content)
