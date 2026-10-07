import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# 1. Student Profile Parent Button
old_student_parent = r'<div x-data="\{ open: \{% if \'Student\' in page_title or \'Enrollment\' in page_title %\}true\{% else %\}false\{% endif %\} \}">\s*<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">'
new_student_parent = """<div x-data="{ open: {% if 'Student' in page_title or 'Enrollment' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Student' in page_title or 'Enrollment' in page_title %}bg-indigo-800 text-white{% endif %}">"""
content = re.sub(old_student_parent, new_student_parent, content)


# 2. Attendance Parent Button
old_attendance_parent = r'<div x-data="\{ open: \{% if \'Attendance\' in page_title %\}true\{% else %\}false\{% endif %\} \}">\s*<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">'
new_attendance_parent = """<div x-data="{ open: {% if 'Attendance' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Attendance' in page_title %}bg-indigo-800 text-white{% endif %}">"""
content = re.sub(old_attendance_parent, new_attendance_parent, content)


# 3. Fees Parent Button
old_fees_parent = r'<div x-data="\{ open: \{% if \'Fee\' in page_title or \'Receipt\' in page_title or \'Refund\' in page_title %\}true\{% else %\}false\{% endif %\} \}">\s*<button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none">'
new_fees_parent = """<div x-data="{ open: {% if 'Fee' in page_title or 'Receipt' in page_title or 'Refund' in page_title %}true{% else %}false{% endif %} }">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none {% if 'Fee' in page_title or 'Receipt' in page_title or 'Refund' in page_title %}bg-indigo-800 text-white{% endif %}">"""
content = re.sub(old_fees_parent, new_fees_parent, content)


# 4. Fix Student Master child button to use bg-indigo-600
old_student_master = r'\{% if page_title == \'Student Master\' or page_title == \'Student Profile\' %\}bg-indigo-800 text-white\{% else %\}hover:bg-indigo-700\{% endif %\}">Student Master'
new_student_master = "{% if page_title == 'Student Master' or page_title == 'Student Profile' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}\">Student Master"
content = re.sub(old_student_master, new_student_master, content)


with open('templates/base.html', 'w') as f:
    f.write(content)
