with open('website/views.py', 'r') as f:
    content = f.read()

import re

# Update create_event redirect
old_redirect = r"return redirect\('/events/\?tab=upcoming'\)"
new_redirect = "return redirect(f'/events/?tab=registration&event_id={event.event_id}')"

# We need to change the create logic to capture the event
old_create = r"EventMaster\.objects\.create\("
new_create = "event = EventMaster.objects.create("

content = re.sub(old_create, new_create, content)
content = re.sub(old_redirect, new_redirect, content)

with open('website/views.py', 'w') as f:
    f.write(content)
