import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

old_back = r'<button @click="tab = \'list\'" class="text-indigo-600 hover:underline flex items-center text-xs mt-1 mr-4">\s*<i class="fa-solid fa-arrow-left mr-1"></i> Back to List\s*</button>'
new_back = '<a href="?tab=list" class="text-indigo-600 hover:underline flex items-center text-xs mt-1 mr-4">\n                    <i class="fa-solid fa-arrow-left mr-1"></i> Back to List\n                </a>'

content = re.sub(old_back, new_back, content)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
