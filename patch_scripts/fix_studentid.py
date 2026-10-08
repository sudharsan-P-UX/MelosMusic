import re

with open('templates/website/students.html', 'r') as f:
    content = f.read()

old_td = """<td class="py-2.5 px-4 flex items-center space-x-2">
                        <i class="fa-regular fa-star text-gray-300 hover:text-yellow-400 cursor-pointer transition"></i>
                        <span class="text-blue-600 cursor-pointer hover:underline">{{ student.display_name }}</span>
                    </td>"""

new_td = """<td class="py-2.5 px-4 text-gray-600 font-medium">{{ student.user_code|default:"-" }}</td>
                    <td class="py-2.5 px-4 flex items-center space-x-2">
                        <i class="fa-regular fa-star text-gray-300 hover:text-yellow-400 cursor-pointer transition"></i>
                        <span class="text-blue-600 cursor-pointer hover:underline">{{ student.display_name }}</span>
                    </td>"""

content = content.replace(old_td, new_td)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
