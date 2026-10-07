import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_edit_mode = r"    edit_mode = request\.GET\.get\('edit', 'false'\) == 'true'\s*if edit_mode:\s*tab = 'create'.*?\s*return render\(request, 'website/events_dashboard\.html', \{"
new_edit_mode = """    edit_mode = request.GET.get('edit', 'false') == 'true'
    
    return render(request, 'website/events_dashboard.html', {
        'edit_mode': edit_mode,"""

content = re.sub(old_edit_mode, new_edit_mode, content, flags=re.DOTALL)

with open('website/views.py', 'w') as f:
    f.write(content)
