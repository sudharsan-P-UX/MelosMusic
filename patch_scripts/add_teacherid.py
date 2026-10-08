import re

with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

# Header
old_teacher_name_th = '<th class="py-3 px-6 font-medium">Name</th>'
new_teacher_name_th = '<th class="py-3 px-6 font-medium">Teacher ID</th>\n                    <th class="py-3 px-6 font-medium">Name</th>'
content = content.replace(old_teacher_name_th, new_teacher_name_th)

# Row
old_teacher_name_td = '<td class="py-3 px-6 border-b font-medium">{{ teacher.first_name }} {{ teacher.last_name }}</td>'
new_teacher_name_td = '<td class="py-3 px-6 border-b font-medium text-blue-600">{{ teacher.user_code|default:"-" }}</td>\n                                  <td class="py-3 px-6 border-b font-medium">{{ teacher.first_name }} {{ teacher.last_name }}</td>'
content = content.replace(old_teacher_name_td, new_teacher_name_td)

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
