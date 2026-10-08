import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Student Profile Dropdown
old_student = """              <div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">"""
new_student = """              {% if user_perms.Student_Profile.view %}
              <div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">"""
content = content.replace(old_student, new_student)

old_student_end = """                      </div>
              </div>"""
# There are multiple of these, so I should just do it carefully using regex or precise strings for the dropdowns.
