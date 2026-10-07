import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update x-data
content = content.replace(
    "showCreateRoleModal: false, showAddUserModal: false",
    "showCreateRoleModal: false, showAddUserModal: false, showMenuModal: false, editMenuData: {id: '', name: '', url: '', active: true}"
)

# 2. Update Add Menu button
content = content.replace(
    """<button class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-plus mr-1"></i> Add Menu
                </button>""",
    """<button @click="editMenuData = {id: '', name: '', url: '#', active: true}; showMenuModal = true" class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-plus mr-1"></i> Add Menu
                </button>"""
)

# 3. Hook up Edit and Delete buttons
old_actions = """<td class="py-1.5 px-4 text-center space-x-2">
                            <button class="text-indigo-400 hover:text-indigo-600 bg-indigo-50 hover:bg-indigo-100 p-1.5 rounded transition"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 p-1.5 rounded transition"><i class="fa-solid fa-trash-can"></i></button>
                        </td>"""

new_actions = """<td class="py-1.5 px-4 text-center space-x-2">
                            <button @click="editMenuData = {id: '{{ m.menu_id }}', name: '{{ m.menu_name }}', url: '{{ m.url_page }}', active: {% if m.is_active %}true{% else %}false{% endif %}}; showMenuModal = true" class="text-indigo-400 hover:text-indigo-600 bg-indigo-50 hover:bg-indigo-100 p-1.5 rounded transition"><i class="fa-solid fa-pen"></i></button>
                            <form method="POST" action="" class="inline-block" onsubmit="return confirm('Are you sure you want to delete this menu? This might break role permissions.');">
                                {% csrf_token %}
                                <input type="hidden" name="action" value="delete_menu">
                                <input type="hidden" name="menu_id" value="{{ m.menu_id }}">
                                <button type="submit" class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 p-1.5 rounded transition"><i class="fa-solid fa-trash-can"></i></button>
                            </form>
                        </td>"""

content = content.replace(old_actions, new_actions)

# 4. Add the Menu Modal at the bottom of the file before </div> (end of x-data div)
modal_html = """
    <!-- Add/Edit Menu Modal -->
    <div x-show="showMenuModal" style="display: none;" class="fixed inset-0 z-[100] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div x-show="showMenuModal" x-transition.opacity class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showMenuModal = false" aria-hidden="true"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div x-show="showMenuModal" x-transition.scale class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <form method="POST" action="">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_menu">
                    <input type="hidden" name="menu_id" x-model="editMenuData.id">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div class="sm:flex sm:items-start">
                            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title" x-text="editMenuData.id ? 'Edit Menu' : 'Add New Menu'"></h3>
                                <div class="mt-4 space-y-4 w-full">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Menu Name</label>
                                        <input type="text" name="menu_name" x-model="editMenuData.name" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">URL Route</label>
                                        <input type="text" name="url_page" x-model="editMenuData.url" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm font-mono text-gray-500">
                                    </div>
                                    <div class="flex items-center mt-4">
                                        <input type="checkbox" name="is_active" x-model="editMenuData.active" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
                                        <label class="ml-2 block text-sm text-gray-900">Active Status</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse border-t border-gray-200">
                        <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm transition" x-text="editMenuData.id ? 'Save Changes' : 'Create Menu'"></button>
                        <button type="button" @click="showMenuModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

content = content.replace("</div>\n{% endblock %}", modal_html)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
