import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Replace the exact button inside the users tab
old_button_pattern = r'(<div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">\s*<h3 class="font-medium text-gray-800">System Users</h3>\s*)<button class="bg-\[\#4f46e5\] text-white[^>]+>\s*<i class="fa-solid fa-user-plus mr-1"></i> Add User\s*</button>'

new_button = r'\1<button @click="showAddUserModal = true" class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">\n                    <i class="fa-solid fa-user-plus mr-1"></i> Add User\n                </button>'

content = re.sub(old_button_pattern, new_button, content)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
