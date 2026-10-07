import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# Pattern to remove the orphaned block
orphaned_pattern = r'                    <div>\s*<label class="block text-xs font-semibold text-gray-600 mb-1">Venue <span class="text-red-500">\*</span></label>.*?<button class="bg-\[#5c4baf\] text-white px-6 py-2 rounded hover:bg-indigo-700 shadow-sm transition">Save Event</button>\s*</div>\s*</div>\s*</div>\s*</div>'

content = re.sub(orphaned_pattern, '', content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
