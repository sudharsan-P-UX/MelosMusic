with open('templates/website/students.html', 'r') as f:
    content = f.read()

import re
old_edit_regex = r'<div class="grid grid-cols-2 gap-4">\s*<div>\s*<label class="block text-sm font-medium text-gray-700 mb-1">Class</label>.*?<div class="grid grid-cols-2 gap-4 mt-4">\s*<div>\s*<label class="block text-sm font-medium text-gray-700 mb-1">Class Time</label>.*?<input type="text" id="modalDays" name="days" .*?>\s*</div>\s*</div>'

content = re.sub(old_edit_regex, '', content, flags=re.DOTALL)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
