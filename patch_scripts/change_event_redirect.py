import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Replace the redirect in create_event_view
old_redirect = "return redirect(f'/events/?tab=details&event_id={event.event_id}')"
new_redirect = "return redirect('/events/?tab=list')"
content = content.replace(old_redirect, new_redirect)

with open('website/views.py', 'w') as f:
    f.write(content)
