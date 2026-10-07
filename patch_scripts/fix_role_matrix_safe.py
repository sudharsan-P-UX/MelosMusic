import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

matrix_start = content.find('        <!-- Role Matrix Editor -->')
matrix_end = content.find('    <!-- User Management Tab -->')

prefix = content[:matrix_start]
suffix = content[matrix_end:]

new_matrix = """        <!-- Role Matrix Editor -->
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-5 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <div>
                    <h3 class="font-medium text-gray-800">Role Permissions Matrix</h3>
                    <p class="text-xs text-gray-500 mt-1">Select a role to configure access</p>
                </div>
                <div class="w-64">
                    <select onchange="window.location.href='?tab=roles&role_id=' + this.value" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white shadow-sm">
                        {% for role in roles %}
                        <option value="{{ role.role_id }}" {% if selected_role and selected_role.role_id == role.role_id %}selected{% endif %}>{{ role.role_name }} ({{ role.role_group.role_group_name }})</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            
            <div class="p-6">
                <div class="mb-6">
                    <h4 class="text-sm font-semibold text-gray-700">Role Name : <span class="font-normal text-indigo-600">{% if selected_role %}{{ selected_role.role_name }}{% else %}Select a role{% endif %}</span></h4>
                    <p class="text-sm text-gray-600 mt-1">Description : <span class="font-normal">{% if selected_role %}{{ selected_role.description|default:"No description" }}{% endif %}</span></p>
                </div>
                <form method="POST" action="">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_permissions">
                    <input type="hidden" name="role_id" value="{{ selected_role.role_id|default:'' }}">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead>
                            <tr class="border-b-2 border-gray-200 text-gray-600 bg-gray-50/50">
                                <th class="py-3 px-4 font-semibold w-1/3">Menu</th>
                                <th class="py-3 px-2 font-semibold text-center">View</th>
                                <th class="py-3 px-2 font-semibold text-center">Add</th>
                                <th class="py-3 px-2 font-semibold text-center">Edit</th>
                                <th class="py-3 px-2 font-semibold text-center">Delete</th>
                                <th class="py-3 px-2 font-semibold text-center">Export</th>
                            </tr>
                        </thead>
                        <tbody class="text-gray-700">
                            {% for menu in menus %}
                            <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                                <td class="py-3 px-4 font-medium text-gray-800"><i class="fa-solid fa-bars text-gray-300 mr-2 text-xs"></i> {{ menu.menu_name }}</td>
                                <td class="py-3 px-2 text-center">
                                    <input type="checkbox" name="view_{{ menu.menu_id }}" {% for k,v in role_access_map.items %}{% if k == menu.menu_id and v.view_access %}checked{% endif %}{% endfor %} class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300">
                                </td>
                                <td class="py-3 px-2 text-center">
                                    <input type="checkbox" name="add_{{ menu.menu_id }}" {% for k,v in role_access_map.items %}{% if k == menu.menu_id and v.add_access %}checked{% endif %}{% endfor %} class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300">
                                </td>
                                <td class="py-3 px-2 text-center">
                                    <input type="checkbox" name="edit_{{ menu.menu_id }}" {% for k,v in role_access_map.items %}{% if k == menu.menu_id and v.edit_access %}checked{% endif %}{% endfor %} class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300">
                                </td>
                                <td class="py-3 px-2 text-center">
                                    <input type="checkbox" name="delete_{{ menu.menu_id }}" {% for k,v in role_access_map.items %}{% if k == menu.menu_id and v.delete_access %}checked{% endif %}{% endfor %} class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300">
                                </td>
                                <td class="py-3 px-2 text-center">
                                    <input type="checkbox" name="export_{{ menu.menu_id }}" {% for k,v in role_access_map.items %}{% if k == menu.menu_id and v.export_access %}checked{% endif %}{% endfor %} class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300">
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    
                    <div class="mt-6 flex justify-end">
                        <button type="submit" class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 transition shadow-sm">
                            <i class="fa-solid fa-check mr-2"></i> Save Role
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
"""

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(prefix + new_matrix + suffix)
