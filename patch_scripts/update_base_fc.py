with open('templates/base.html', 'r') as f:
    content = f.read()

old_fc = """<a href="{% url 'generic_page' 'fee-collection' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Collection' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>"""
new_fc = """<a href="{% url 'fee_collection' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Fee Collection' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Fee Collection</a>"""

content = content.replace(old_fc, new_fc)

with open('templates/base.html', 'w') as f:
    f.write(content)
