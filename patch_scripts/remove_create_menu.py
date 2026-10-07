import re

with open('templates/base.html', 'r') as f:
    content = f.read()

content = re.sub(
    r'<a href="{% url \'events_dashboard\' %}\?tab=create" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Create Event</a>\s*',
    '',
    content
)

with open('templates/base.html', 'w') as f:
    f.write(content)
