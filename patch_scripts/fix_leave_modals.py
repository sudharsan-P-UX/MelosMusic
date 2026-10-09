import re

with open('templates/website/student_attendance.html', 'r') as f:
    content = f.read()

# Fix student modal
old_s_option = """<option value="{{ s.user.user_id }}" {% if user.user_id == s.user.user_id %}selected{% endif %}>{{ s.user.display_name|default:s.user.first_name }}</option>"""
new_s_option = """<option value="{{ s.user_id }}" {% if user.user_id == s.user_id %}selected{% endif %}>{{ s.display_name|default:s.first_name }}</option>"""
content = content.replace(old_s_option, new_s_option)

with open('templates/website/student_attendance.html', 'w') as f:
    f.write(content)

with open('templates/website/teacher_attendance.html', 'r') as f:
    content = f.read()

# Fix teacher modal
old_t_option = """<option value="{{ t.user.user_id }}" {% if user.user_id == t.user.user_id %}selected{% endif %}>{{ t.user.display_name|default:t.user.first_name }}</option>"""
new_t_option = """<option value="{{ t.user_id }}" {% if user.user_id == t.user_id %}selected{% endif %}>{{ t.display_name|default:t.first_name }}</option>"""
content = content.replace(old_t_option, new_t_option)

with open('templates/website/teacher_attendance.html', 'w') as f:
    f.write(content)
