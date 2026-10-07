with open('templates/base.html', 'r') as f:
    content = f.read()

old_attendance = '''            <a href="{% url 'generic_page' 'attendance' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Attendance' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Attendance</a>'''
new_attendance = '''            <div x-data="{ open: {% if 'Attendance' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">
                    <span>Attendance</span>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                </button>
                <div x-show="open" class="pl-4 mt-1 space-y-1">
                    <a href="{% url 'student_attendance' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Attendance' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Student Attendance</a>
                    <a href="{% url 'teacher_attendance' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Teacher Attendance' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Teacher Attendance</a>
                </div>
            </div>'''
content = content.replace(old_attendance, new_attendance)

# Add alpine.js to base.html if not already there (it makes dropdowns trivial)
if 'alpinejs' not in content:
    content = content.replace('</head>', '    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>\n</head>')

with open('templates/base.html', 'w') as f:
    f.write(content)
