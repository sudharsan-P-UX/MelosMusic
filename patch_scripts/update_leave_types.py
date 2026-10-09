import re

with open('templates/website/student_attendance.html', 'r') as f:
    content = f.read()

old_options = """<option value="Sick Leave">Sick Leave</option>
                        <option value="Casual Leave">Casual Leave</option>
                        <option value="Emergency Leave">Emergency Leave</option>
                        <option value="Vacation">Vacation</option>"""

new_options = """<option value="On Duty">On Duty</option>
                        <option value="Permission">Permission</option>
                        <option value="Work From Home">Work From Home</option>
                        <option value="Work From Office">Work From Office</option>
                        <option value="Leave">Leave</option>"""

content = content.replace(old_options, new_options)

with open('templates/website/student_attendance.html', 'w') as f:
    f.write(content)

with open('templates/website/teacher_attendance.html', 'r') as f:
    content = f.read()

content = content.replace(old_options, new_options)

with open('templates/website/teacher_attendance.html', 'w') as f:
    f.write(content)
