import re

with open('website/views.py', 'r') as f:
    content = f.read()

# I need to add JsonResponse at the top, or inside the functions
content = content.replace(
    'def api_get_student_details(request):',
    'from django.http import JsonResponse\ndef api_get_student_details(request):'
)

content = content.replace(
    'def api_get_batch_details(request):',
    'from django.http import JsonResponse\ndef api_get_batch_details(request):'
)

with open('website/views.py', 'w') as f:
    f.write(content)
