with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

import re

old_buttons = r'<div x-show="tab === \'registration\'">\s*<button class="bg-\[#5c4baf\] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs">\s*<i class="fa-solid fa-plus mr-1.5"></i> Add Participant\s*</button>\s*</div>'

new_buttons = """<div class="flex space-x-3">
            <button x-show="tab === 'registration'" class="bg-[#5c4baf] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Participant
            </button>
            <button x-show="tab !== 'create'" @click="tab = 'create'" class="bg-[#0066cc] hover:bg-blue-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Event
            </button>
        </div>"""

content = re.sub(old_buttons, new_buttons, content)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
