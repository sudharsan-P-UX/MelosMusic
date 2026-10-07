import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update the role select dropdown to reload the page
select_old = r'<select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white shadow-sm">\s*{% for role in roles %}\s*<option value="{{ role.role_id }}">{{ role.role_name }} \({{ role.role_group.role_group_name }}\)</option>\s*{% endfor %}\s*</select>'
select_new = """<select onchange="window.location.href='?tab=roles&role_id=' + this.value" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white shadow-sm">
                        {% for role in roles %}
                        <option value="{{ role.role_id }}" {% if selected_role and selected_role.role_id == role.role_id %}selected{% endif %}>{{ role.role_name }} ({{ role.role_group.role_group_name }})</option>
                        {% endfor %}
                    </select>"""
content = re.sub(select_old, select_new, content)

# 2. Update Role display
role_display_old = r'<h4 class="text-sm font-semibold text-gray-700">Role Name : <span class="font-normal text-indigo-600">Teacher</span></h4>\s*<p class="text-sm text-gray-600 mt-1">Description : <span class="font-normal">Music Teacher</span></p>'
role_display_new = """<h4 class="text-sm font-semibold text-gray-700">Role Name : <span class="font-normal text-indigo-600">{% if selected_role %}{{ selected_role.role_name }}{% endif %}</span></h4>
                    <p class="text-sm text-gray-600 mt-1">Description : <span class="font-normal">{% if selected_role %}{{ selected_role.description|default:"No description" }}{% endif %}</span></p>"""
content = re.sub(role_display_old, role_display_new, content)

# 3. Wrap the table in a form and update the loop to use role_access_map
table_old = r'<table class="w-full text-left border-collapse text-sm">([\s\S]*?)</table>'

# We need to construct the new table with the form and the loop
table_new_inner = """<form method="POST" action="">
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
                </form>"""

content = re.sub(table_old, table_new_inner, content)

# Remove the old Save Role button which was outside the table
old_save_btn = r'<div class="mt-6 flex justify-end">\s*<button class="bg-\[\#4f46e5\] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 transition shadow-sm">\s*<i class="fa-solid fa-check mr-2"></i> Save Role\s*</button>\s*</div>'
content = re.sub(old_save_btn, '', content)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
