import re
with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# Make form a flex container
content = content.replace(
    '<form method="POST" action="{% url \'courses\' %}">',
    '<form method="POST" action="{% url \'courses\' %}" class="flex flex-col flex-1 overflow-hidden">'
)

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
