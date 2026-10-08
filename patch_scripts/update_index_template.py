import re

with open('templates/website/index.html', 'r') as f:
    content = f.read()

# Replace hardcoded values with variables
content = content.replace(
    '<div class="text-3xl font-bold text-slate-800 mt-2">1,245</div>',
    '<div class="text-3xl font-bold text-slate-800 mt-2">{{ total_students|default:"0" }}</div>'
)

content = content.replace(
    '<div class="text-3xl font-bold text-slate-800 mt-2">32</div>',
    '<div class="text-3xl font-bold text-slate-800 mt-2">{{ active_teachers|default:"0" }}</div>'
)

content = content.replace(
    '<div class="text-3xl font-bold text-slate-800 mt-2">15</div>',
    '<div class="text-3xl font-bold text-slate-800 mt-2">{{ total_courses|default:"0" }}</div>'
)

content = content.replace(
    '<div class="text-3xl font-bold text-red-600 mt-2">$4,300</div>',
    '<div class="text-3xl font-bold text-red-600 mt-2">${{ pending_fees|floatformat:2|default:"0.00" }}</div>'
)

with open('templates/website/index.html', 'w') as f:
    f.write(content)
