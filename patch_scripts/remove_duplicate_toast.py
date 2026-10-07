import re

with open('templates/base.html', 'r') as f:
    content = f.read()

start_idx = content.find('    <!-- Toast Messages -->')
if start_idx != -1:
    end_idx = content.find('    <!-- Restore Sidebar Scroll Position -->', start_idx)
    if end_idx != -1:
        content = content[:start_idx] + content[end_idx:]

with open('templates/base.html', 'w') as f:
    f.write(content)
