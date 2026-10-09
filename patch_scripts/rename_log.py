import re

with open('templates/website/attendance_log.html', 'r') as f:
    content = f.read()

content = content.replace('Leave Requests', 'Attendance Requests')
content = content.replace('No leave requests found.', 'No attendance requests found.')

with open('templates/website/attendance_log.html', 'w') as f:
    f.write(content)
