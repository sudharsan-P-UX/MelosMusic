import re

with open('templates/website/index.html', 'r') as f:
    content = f.read()

# Replace hardcoded values with variables using regex
content = re.sub(r'<p class="text-3xl font-bold text-gray-800 mt-2">1,245</p>', r'<p class="text-3xl font-bold text-gray-800 mt-2">{{ total_students|default:"0" }}</p>', content)
content = re.sub(r'<p class="text-3xl font-bold text-gray-800 mt-2">32</p>', r'<p class="text-3xl font-bold text-gray-800 mt-2">{{ active_teachers|default:"0" }}</p>', content)
content = re.sub(r'<p class="text-3xl font-bold text-gray-800 mt-2">15</p>', r'<p class="text-3xl font-bold text-gray-800 mt-2">{{ total_courses|default:"0" }}</p>', content)
content = re.sub(r'<p class="text-3xl font-bold text-red-600 mt-2">\$4,300</p>', r'<p class="text-3xl font-bold text-red-600 mt-2">${{ pending_fees|floatformat:2|default:"0.00" }}</p>', content)

with open('templates/website/index.html', 'w') as f:
    f.write(content)
