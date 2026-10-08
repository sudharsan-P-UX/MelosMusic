import re

with open('templates/website/students.html', 'r') as f:
    content = f.read()

# Header
old_student_name_th = '<th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100 flex items-center">Student Name <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>'
new_student_name_th = '<th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Student ID <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>\n                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100 flex items-center">Student Name <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>'
content = content.replace(old_student_name_th, new_student_name_th)

# Row
old_student_name_td = """<td class="py-2 px-4 border-b border-gray-100">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs mr-3 shadow-sm border border-blue-200">"""
new_student_name_td = """<td class="py-2 px-4 border-b border-gray-100 font-medium text-blue-600">{{ student.user_code|default:"-" }}</td>
                        <td class="py-2 px-4 border-b border-gray-100">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-xs mr-3 shadow-sm border border-blue-200">"""
content = content.replace(old_student_name_td, new_student_name_td)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
