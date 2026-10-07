with open('templates/base.html', 'r') as f:
    content = f.read()

import re
old_link = r'<a href="{% url \'students\' %}" class="block px-4 py-2 rounded-md.*?">Student Profile</a>'

new_dropdown = """<div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">
                    <span>Student Profile</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    <a href="{% url 'students' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Master' or page_title == 'Student Profile' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>
                    <a href="{% url 'generic_page' 'enrollment_management' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Enrollment Management' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Enrollment Management</a>
                    <a href="{% url 'student_attendance' %}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Attendance</a>
                    <a href="{% url 'fee_dashboard' %}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Fees</a>
                    <a href="{% url 'reports' %}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Student Reports</a>
                </div>
            </div>"""

content = re.sub(old_link, new_dropdown, content)

with open('templates/base.html', 'w') as f:
    f.write(content)
