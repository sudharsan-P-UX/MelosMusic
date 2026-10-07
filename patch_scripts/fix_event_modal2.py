import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Replace `tab == 'create'` with `active_tab == 'create'`
content = content.replace("tab == 'create'", "active_tab == 'create'")

# 2. Update the Cancel button in the modal
old_cancel = r'<button type="button" @click="showCreateModal = false" class="border border-gray-300 bg-white text-gray-700 px-8 py-2\.5 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>'
new_cancel = '<a href="?tab=list" class="border border-gray-300 bg-white text-gray-700 px-8 py-2.5 rounded text-sm font-medium hover:bg-gray-50 transition inline-flex items-center justify-center">Cancel</a>'
content = re.sub(old_cancel, new_cancel, content)

# 3. Remove Edit and Delete buttons from the 'details' tab header
old_details_buttons = r'<div x-show="tab === \'details\'" class="flex space-x-2">\s*<button @click="showCreateModal = true".*?>\s*<i class="fa-solid fa-pen mr-1\.5"></i> Edit\s*</button>\s*<button class="bg-red-500 hover:bg-red-600 text-white px-4 py-1\.5 rounded shadow-sm flex items-center text-xs transition">\s*<i class="fa-solid fa-trash-can mr-1\.5"></i> Delete\s*</button>\s*</div>'
content = re.sub(old_details_buttons, '', content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
