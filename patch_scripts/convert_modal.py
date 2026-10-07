import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update x-data to include modal state
old_xdata = r'x-data="\{ tab: \'\{\{ active_tab\|default:\'calendar\' \}\}\' \}"'
new_xdata = 'x-data="{ tab: \'{{ active_tab|default:\'list\' }}\', showCreateModal: {% if tab == \'create\' %}true{% else %}false{% endif %} }"'
content = re.sub(old_xdata, new_xdata, content)

# 2. Update Add Event buttons to open modal instead of changing tab
old_add_btn1 = r'<button x-show="\[\'list\', \'upcoming\', \'calendar\'\]\.includes\(tab\)" @click="tab = \'create\'" class="bg-\[#4f46e5\] hover:bg-indigo-700 text-white px-4 py-1\.5 rounded shadow-sm flex items-center text-xs transition">\s*<i class="fa-solid fa-plus mr-1\.5"></i> Add Event\s*</button>'
new_add_btn1 = """<button x-show="['list', 'upcoming', 'calendar'].includes(tab)" @click="showCreateModal = true" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Event
            </button>"""
content = re.sub(old_add_btn1, new_add_btn1, content)

old_edit_btn = r'<button @click="tab = \'create\'" class="bg-\[#4f46e5\] hover:bg-indigo-700 text-white px-4 py-1\.5 rounded shadow-sm flex items-center text-xs transition">\s*<i class="fa-solid fa-pen mr-1\.5"></i> Edit\s*</button>'
new_edit_btn = """<button @click="showCreateModal = true" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                    <i class="fa-solid fa-pen mr-1.5"></i> Edit
                </button>"""
content = re.sub(old_edit_btn, new_edit_btn, content)

old_table_edit = r'<a href="\?tab=create&event_id=\{\{ ev\.event_id \}\}" class="w-7 h-7 rounded-full bg-blue-50 text-blue-500 flex items-center justify-center hover:bg-blue-100 transition"><i class="fa-solid fa-pen text-\[10px\]"></i></a>'
new_table_edit = '<a href="?tab=list&event_id={{ ev.event_id }}&edit=true" class="w-7 h-7 rounded-full bg-blue-50 text-blue-500 flex items-center justify-center hover:bg-blue-100 transition"><i class="fa-solid fa-pen text-[10px]"></i></a>'
content = re.sub(old_table_edit, new_table_edit, content)

# 3. Wrap the form in a modal UI
# Find the start of the form
form_start_match = re.search(r'<form method="POST" action="{% url \'create_event\' %}" class="bg-white p-8 rounded shadow-sm border border-gray-200 max-w-5xl">', content)
form_end_match = re.search(r'</form>', content[form_start_match.start():])

if form_start_match and form_end_match:
    start_idx = form_start_match.start()
    end_idx = start_idx + form_end_match.end()
    
    original_form = content[start_idx:end_idx]
    
    # Modify the form slightly for the modal
    modal_form = original_form.replace(
        '<form method="POST" action="{% url \'create_event\' %}" class="bg-white p-8 rounded shadow-sm border border-gray-200 max-w-5xl">',
        '<form method="POST" action="{% url \'create_event\' %}" class="bg-white p-8 rounded shadow-lg max-w-5xl w-full max-h-[90vh] overflow-y-auto" @click.stop>'
    )
    
    # Change the cancel button in the form
    modal_form = re.sub(
        r'<button type="button" @click="tab = \'list\'".*?>Cancel</button>',
        '<button type="button" @click="showCreateModal = false" class="border border-gray-300 bg-white text-gray-700 px-8 py-2.5 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>',
        modal_form
    )
    
    # Add modal wrapper
    modal_wrapper = f"""<!-- Create/Edit Modal -->
        <div x-show="showCreateModal" style="display: none;" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm transition-opacity" @click="showCreateModal = false">
            {modal_form}
        </div>"""
        
    content = content[:start_idx] + modal_wrapper + content[end_idx:]

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)

