import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Pattern to match the specific "Student Attendance" block under "Student Profile"
# We'll replace the Enrollment Management followed by Student Attendance with just Enrollment Management
old_pattern = r'(<a href="\{% url \'enrollment_management\' %\}" class="block px-4 py-2 text-sm rounded-md \{% if page_title == \'Enrollment Management\' %\}bg-indigo-600 text-white font-medium\{% else %\}hover:bg-indigo-700\{% endif %\}"\>Enrollment Management</a>)\s*<a href="\{% url \'student_attendance\' %\}" class="block px-4 py-2 text-sm rounded-md \{% if page_title == \'Student Attendance\' %\}bg-indigo-600 text-white font-medium\{% else %\}hover:bg-indigo-700\{% endif %\}">Student Attendance</a>'

new_pattern = r'\1'

content = re.sub(old_pattern, new_pattern, content)

with open('templates/base.html', 'w') as f:
    f.write(content)
