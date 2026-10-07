import re

with open('website/views.py', 'r') as f:
    content = f.read()

start = content.find('def students_view(request):')
end = content.find('def generic_page(request, page_name):')
student_code = content[start:end]

t_code = student_code.replace('students_view', 'teachers_view')
t_code = t_code.replace('students.html', 'teachers.html')
t_code = t_code.replace('Student Profile', 'Teacher Management')
t_code = t_code.replace("'students'", "'teachers'")
t_code = t_code.replace('student_name', 'teacher_name')
t_code = t_code.replace('update_student', 'update_teacher')
t_code = t_code.replace('delete_student', 'delete_teacher')
t_code = t_code.replace('student_role', 'teacher_role')
t_code = t_code.replace('new_student', 'new_teacher')
t_code = t_code.replace('student = ', 'teacher = ')
t_code = t_code.replace('student.', 'teacher.')
t_code = t_code.replace('student_id', 'teacher_id')
t_code = t_code.replace('"Students"', '"Teachers"')
t_code = t_code.replace('"Student"', '"Teacher"')
t_code = t_code.replace('students = ', 'teachers = ')
t_code = t_code.replace("'students':", "'teachers':")

new_content = content[:end] + t_code + '\n' + content[end:]
with open('website/views.py', 'w') as f:
    f.write(new_content)

with open('templates/website/students.html', 'r') as f:
    html = f.read()

html = html.replace('Student Profile', 'Teacher Management')
html = html.replace('Add Student', 'Add Teacher')
html = html.replace('Students Directory', 'Teachers Directory')
html = html.replace('Student Name', 'Teacher Name')
html = html.replace('Save Student', 'Save Teacher')
html = html.replace('Update Student', 'Update Teacher')
html = html.replace('student.', 'teacher.')
html = html.replace("'students'", "'teachers'")
html = html.replace('student_name', 'teacher_name')
html = html.replace('addStudentModal', 'addTeacherModal')
html = html.replace('studentForm', 'teacherForm')
html = html.replace('update_student', 'update_teacher')
html = html.replace('delete_student', 'delete_teacher')

with open('templates/website/teachers.html', 'w') as f:
    f.write(html)
