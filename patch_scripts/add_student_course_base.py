import re

with open('templates/base.html', 'r') as f:
    content = f.read()

old_menu_link = """{% if user_perms.Student_Master.view or user_perms.Student_Profile.view %}<a href="{% url 'students' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Master' or page_title == 'Student Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>{% endif %}"""

new_menu_link = """{% if user_perms.Student_Master.view or user_perms.Student_Profile.view %}<a href="{% url 'students' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Master' or page_title == 'Student Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Master</a>{% endif %}
                    {% if user_perms.Student_Course.view or user_perms.Student_Profile.view %}<a href="{% url 'student_course' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Course' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Course</a>{% endif %}"""

content = content.replace(old_menu_link, new_menu_link)

with open('templates/base.html', 'w') as f:
    f.write(content)
