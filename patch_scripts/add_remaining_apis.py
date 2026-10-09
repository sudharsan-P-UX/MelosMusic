import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

api_code = """
@csrf_exempt
def mobile_events_api(request):
    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': [{'event_name': 'Annual Day', 'date': '2026-12-01'}]})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def mobile_settings_api(request):
    if request.method == 'GET':
        return JsonResponse({'success': True, 'data': [{'setting': 'Theme', 'value': 'Light'}, {'setting': 'Version', 'value': '1.0'}]})
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
"""

text += api_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
