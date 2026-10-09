import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import MasterMenu

# 1. Update MasterMenu URL
menu = MasterMenu.objects.filter(menu_name='Teacher Class Allocation').first()
if menu:
    menu.url_page = '/teacher-allocation/'
    menu.save()

# 2. Update urls.py
with open('website/urls.py', 'r') as f:
    urls_content = f.read()

if "path('teacher-allocation/'" not in urls_content:
    urls_content = urls_content.replace(
        "path('student-allocation/', views.student_allocation_view, name='student_allocation'),",
        "path('student-allocation/', views.student_allocation_view, name='student_allocation'),\n    path('teacher-allocation/', views.teacher_allocation_view, name='teacher_allocation'),\n    path('api/get-teacher/', views.api_get_teacher_details, name='api_get_teacher'),"
    )
    with open('website/urls.py', 'w') as f:
        f.write(urls_content)

# 3. Update base.html
with open('templates/base.html', 'r') as f:
    base_content = f.read()

old_link = """{% if user_perms.Teacher_Class_Allocation.view or user_perms.Administration.view %}
                    <a href="{% url 'generic_page' 'teacher-class-allocation' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Teacher Class Allocation' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Class Allocation</a>
                    {% endif %}"""

new_link = """{% if user_perms.Teacher_Class_Allocation.view or user_perms.Administration.view %}
                    <a href="{% url 'teacher_allocation' %}" class="block px-4 py-2 text-sm rounded-md {% if page_title == 'Teacher Class Allocation' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Teacher Class Allocation</a>
                    {% endif %}"""

base_content = base_content.replace(old_link, new_link)
with open('templates/base.html', 'w') as f:
    f.write(base_content)

print("Setup URLs and base.html for Teacher Allocation")
