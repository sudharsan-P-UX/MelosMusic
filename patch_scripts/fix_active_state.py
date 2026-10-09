import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Fix the open state and active background for the Student Profile dropdown
old_div = """<div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Student' in page_title or 'Enrollment' in page_title %}bg-indigo-800 text-white{% endif %}">"""

new_div = """<div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title or 'Allocation Details' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Student' in page_title or 'Enrollment' in page_title or 'Allocation Details' in page_title %}bg-indigo-800 text-white{% endif %}">"""

content = content.replace(old_div, new_div)

with open('templates/base.html', 'w') as f:
    f.write(content)
