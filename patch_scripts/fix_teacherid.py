import re

with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

old_td = """<td class="py-4 px-6 font-medium">{{ teacher.display_name }}</td>"""
new_td = """<td class="py-4 px-6 font-medium text-gray-600">{{ teacher.user_code|default:"-" }}</td>
                    <td class="py-4 px-6 font-medium">{{ teacher.display_name }}</td>"""

content = content.replace(old_td, new_td)

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
