import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# I need to separate the form header, body, and footer so the footer can stick.
# Original:
# <form method="POST" action="{% url 'create_event' %}" class="bg-white p-8 rounded shadow-lg max-w-5xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
#     {% csrf_token %}
#     ...
#     <div class="flex justify-end space-x-4 mt-8 pt-6"> ... </div>
# </form>

old_form_start = r'<form method="POST" action="{% url \'create_event\' %}" class="bg-white p-8 rounded shadow-lg max-w-5xl w-full max-h-\[90vh\] overflow-y-auto" @click\.stop>'
new_form_start = """<form method="POST" action="{% url 'create_event' %}" class="bg-white rounded shadow-lg max-w-5xl w-full max-h-[90vh] flex flex-col relative" @click.stop>
                <div class="px-8 py-5 border-b border-gray-200 bg-gray-50 flex justify-between items-center rounded-t">
                    <h3 class="text-lg font-medium text-gray-800" x-text="tab === 'create' && selected_event ? 'Edit Event' : 'Add Event'"></h3>
                    <button type="button" @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600 transition">
                        <i class="fa-solid fa-xmark text-lg"></i>
                    </button>
                </div>
                <div class="p-8 overflow-y-auto flex-1">"""

content = re.sub(old_form_start, new_form_start, content)


old_form_end = r'<!-- Action Buttons -->\s*<div class="flex justify-end space-x-4 mt-8 pt-6">\s*<button type="button" @click="showCreateModal = false" class="border border-gray-300 bg-white text-gray-700 px-8 py-2\.5 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>\s*<button type="submit" class="bg-\[#4f46e5\] text-white px-8 py-2\.5 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">\{% if selected_event and tab == \'create\' %\}Save Changes\{% else %\}Add Event\{% endif %\}</button>\s*</div>\s*</form>'

new_form_end = """</div>
                <!-- Action Buttons -->
                <div class="px-8 py-4 border-t border-gray-200 bg-gray-50 flex justify-end space-x-4 rounded-b">
                    <button type="button" @click="showCreateModal = false" class="border border-gray-300 bg-white text-gray-700 px-8 py-2.5 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>
                    <button type="submit" class="bg-[#4f46e5] text-white px-8 py-2.5 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">{% if selected_event and tab == 'create' %}Save Changes{% else %}Add Event{% endif %}</button>
                </div>
            </form>"""

content = re.sub(old_form_end, new_form_end, content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
