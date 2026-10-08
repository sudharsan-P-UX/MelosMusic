import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Courses & Batches
content = content.replace(
    '<a href="{% url \'courses\' %}" class="block px-4 py-2 rounded-md {% if page_title == \'Courses & Batches\' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Courses & Batches</a>',
    '{% if user_perms.Courses_and_Batches.view %}<a href="{% url \'courses\' %}" class="block px-4 py-2 rounded-md {% if page_title == \'Courses & Batches\' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Courses & Batches</a>{% endif %}'
)
# Note: In database, it's "Courses & Batches", so `replace(' ', '_')` makes it `Courses_&_Batches`. Wait, am I accessing `user_perms.Courses_&_Batches`? That's invalid Django template syntax!
# Django template variable names cannot contain `&`.
