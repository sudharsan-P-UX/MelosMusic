import re

with open('website/views.py', 'r') as f:
    content = f.read()

# I want to modify events_dashboard_view to handle the edit parameter
old_view = r"elif events\.exists\(\):\s*selected_event = events\.first\(\)"
new_view = """elif events.exists():
        selected_event = events.first()
        
    edit_mode = request.GET.get('edit', 'false') == 'true'
    if edit_mode:
        tab = 'create' # To trigger modal opening in template via {% if tab == 'create' %}"""

content = re.sub(old_view, new_view, content)

with open('website/views.py', 'w') as f:
    f.write(content)
