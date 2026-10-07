import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Fix Student Attendance under Student Profile
old_att = r'<a href="\{% url \'student_attendance\' %\}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Attendance</a>'
new_att = '<a href="{% url \'student_attendance\' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == \'Student Attendance\' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Attendance</a>'

content = re.sub(old_att, new_att, content)

with open('templates/base.html', 'w') as f:
    f.write(content)
