with open('templates/base.html', 'r') as f:
    content = f.read()

old_af = """<a href="{% url 'generic_page' 'assign-fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Assign Fees' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>"""
new_af = """<a href="{% url 'assign_fees' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Assign Fees' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Assign Fees</a>"""

content = content.replace(old_af, new_af)

with open('templates/base.html', 'w') as f:
    f.write(content)
