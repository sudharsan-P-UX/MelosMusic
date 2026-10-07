import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_thead_tr = '<tr class="border-b-2 border-gray-200 text-gray-600 bg-gray-50/50">'
new_thead_tr = '<tr class="border-b-2 border-gray-200 text-gray-600 bg-gray-50/90 backdrop-blur sticky top-0 z-10 shadow-sm">'

content = content.replace(old_thead_tr, new_thead_tr)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
