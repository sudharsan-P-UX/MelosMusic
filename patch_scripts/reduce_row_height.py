import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Replace all table cell vertical padding (py-3) with (py-1.5)
# Using regex to target standard table tags
content = re.sub(r'(<t[hd][^>]*class="[^"]*)py-3', r'\1py-1.5', content)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
