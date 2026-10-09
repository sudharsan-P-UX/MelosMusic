import re

# Update views.py
with open('website/views.py', 'r') as f:
    views_content = f.read()

views_content = views_content.replace('student.mobile_number', 'student.phone')
views_content = views_content.replace('batch.teacher.mobile_number', 'batch.teacher.phone')

with open('website/views.py', 'w') as f:
    f.write(views_content)

# Update student_allocation.html
with open('templates/website/student_allocation.html', 'r') as f:
    html_content = f.read()

html_content = html_content.replace('alloc.student.mobile_number', 'alloc.student.phone')
html_content = html_content.replace('alloc.batch.teacher.mobile_number', 'alloc.batch.teacher.phone')

with open('templates/website/student_allocation.html', 'w') as f:
    f.write(html_content)

print("Fixed mobile_number to phone!")
