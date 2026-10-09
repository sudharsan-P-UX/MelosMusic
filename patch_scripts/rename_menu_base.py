import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Replace Student Course with Allocation Details for the link text and RBAC permission checks
content = content.replace(
    """{% if user_perms.Student_Course.view or user_perms.Student_Profile.view %}<a href="{% url 'student_course' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Student Course' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Student Course</a>{% endif %}""",
    """{% if user_perms.Allocation_Details.view or user_perms.Student_Course.view or user_perms.Student_Profile.view %}<a href="{% url 'student_course' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Allocation Details' or page_title == 'Student Course' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Allocation Details</a>{% endif %}"""
)

with open('templates/base.html', 'w') as f:
    f.write(content)
