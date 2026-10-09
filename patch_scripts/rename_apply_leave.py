import re

with open('templates/website/student_attendance.html', 'r') as f:
    content = f.read()

content = content.replace('Apply Leave', 'Attendance Request')
content = content.replace('Apply for Leave', 'Submit Attendance Request')
content = content.replace('Leave Type', 'Request Type')

with open('templates/website/student_attendance.html', 'w') as f:
    f.write(content)

with open('templates/website/teacher_attendance.html', 'r') as f:
    content = f.read()

content = content.replace('Apply Leave', 'Attendance Request')
content = content.replace('Apply for Leave', 'Submit Attendance Request')
content = content.replace('Leave Type', 'Request Type')

with open('templates/website/teacher_attendance.html', 'w') as f:
    f.write(content)
