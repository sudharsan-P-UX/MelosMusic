import re

def hide_filters(filepath, role_to_hide):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Select Batch and Select Student or Select Teacher
    if role_to_hide == 'Student':
        # Wrap the filters in {% if user.role.role_name != 'Student' %}
        pattern = r'(<div class="w-48">\s*<select name="batch_id".*?</select>\s*</div>\s*<div class="w-48">\s*<select name="student_id".*?</select>\s*</div>)'
        content = re.sub(pattern, r"{% if user.role.role_name != 'Student' %}\1{% endif %}", content, flags=re.DOTALL)
    elif role_to_hide == 'Teacher':
        pattern = r'(<div class="w-48">\s*<select name="teacher_id".*?</select>\s*</div>)'
        content = re.sub(pattern, r"{% if user.role.role_name != 'Teacher' %}\1{% endif %}", content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

hide_filters('templates/website/student_attendance_v2.html', 'Student')
hide_filters('templates/website/teacher_attendance_v2.html', 'Teacher')
