import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update editMenuData x-data
content = content.replace(
    "editMenuData: {id: '', name: '', url: '', active: true}",
    "editMenuData: {id: '', name: '', url: '', parent_id: '', active: true}"
)

# 2. Update Add Menu button
content = content.replace(
    "@click=\"editMenuData = {id: '', name: '', url: '#', active: true}; showMenuModal = true\"",
    "@click=\"editMenuData = {id: '', name: '', url: '#', parent_id: '', active: true}; showMenuModal = true\""
)

# 3. Update Edit Menu button in the loop
content = content.replace(
    "editMenuData = {id: '{{ m.menu_id }}', name: '{{ m.menu_name }}', url: '{{ m.url_page }}', active: {% if m.is_active %}true{% else %}false{% endif %}};",
    "editMenuData = {id: '{{ m.menu_id }}', name: '{{ m.menu_name }}', url: '{{ m.url_page }}', parent_id: '{{ m.parent_menu_id|default:'' }}', active: {% if m.is_active %}true{% else %}false{% endif %}};"
)

# 4. Add Parent Menu dropdown to the modal
old_modal_inputs = """                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">URL Route</label>
                                        <input type="text" name="url_page" x-model="editMenuData.url" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm font-mono text-gray-500">
                                    </div>"""

new_modal_inputs = """                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">URL Route</label>
                                        <input type="text" name="url_page" x-model="editMenuData.url" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm font-mono text-gray-500">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Parent Menu (Optional)</label>
                                        <select name="parent_menu_id" x-model="editMenuData.parent_id" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                                            <option value="">-- None (Top Level) --</option>
                                            {% for m in menus %}
                                            <template x-if="editMenuData.id != '{{ m.menu_id }}'">
                                                <option value="{{ m.menu_id }}">{{ m.menu_name }}</option>
                                            </template>
                                            {% endfor %}
                                        </select>
                                    </div>"""

content = content.replace(old_modal_inputs, new_modal_inputs)

# 5. Display the parent menu name in the Menu Master List
old_menu_td = '<td class="py-1.5 px-4 font-medium text-gray-800"><i class="fa-solid fa-folder text-gray-300 mr-2"></i> {{ m.menu_name }}</td>'
new_menu_td = '<td class="py-1.5 px-4 font-medium text-gray-800">{% if m.parent_menu %}<i class="fa-solid fa-level-up-alt fa-rotate-90 text-gray-300 ml-4 mr-2"></i>{% else %}<i class="fa-solid fa-folder text-gray-300 mr-2"></i>{% endif %} {{ m.menu_name }}{% if m.parent_menu %} <span class="text-xs text-gray-400 font-normal ml-2">({{ m.parent_menu.menu_name }})</span>{% endif %}</td>'

content = content.replace(old_menu_td, new_menu_td)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
