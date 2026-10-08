import re

with open('templates/website/students.html', 'r') as f:
    content = f.read()
content = content.replace('colspan="7"', 'colspan="8"')
with open('templates/website/students.html', 'w') as f:
    f.write(content)

with open('templates/website/teachers.html', 'r') as f:
    content = f.read()
content = content.replace('colspan="6"', 'colspan="7"')
with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
