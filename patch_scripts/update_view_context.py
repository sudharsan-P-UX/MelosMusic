with open('website/views.py', 'r') as f:
    content = f.read()

import re

old_view_start = r"tab = request\.GET\.get\('tab', 'calendar'\)"

new_view_start = """tab = request.GET.get('tab', 'calendar')
    
    event_id = request.GET.get('event_id')
    selected_event = None
    if event_id:
        try:
            selected_event = EventMaster.objects.get(event_id=event_id)
        except:
            pass
    elif events.exists():
        selected_event = events.first()"""

content = re.sub(old_view_start, new_view_start, content)

# And add selected_event to context
old_context = r"'active_tab': tab"
new_context = "'active_tab': tab,\n        'selected_event': selected_event"

content = re.sub(old_context, new_context, content)

with open('website/views.py', 'w') as f:
    f.write(content)
