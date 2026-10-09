import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Rename 'menu': 'Menu Permissions' to 'Menu Details'
content = content.replace("'menu': 'Menu Permissions',", "'menu': 'Menu Details',")

# 2. Rename tab title
content = content.replace("<!-- Menu Permissions Tab -->", "<!-- Menu Details Tab -->")
content = content.replace("Menu Master List", "Menu Details List")

# 3. Add OrderList column header
old_menu_header = """<th class="py-1.5 px-4 font-medium w-16 text-center">ID</th>
                        <th class="py-1.5 px-4 font-medium">Menu Name</th>
                        <th class="py-1.5 px-4 font-medium">URL Route</th>"""
new_menu_header = """<th class="py-1.5 px-4 font-medium w-16 text-center">ID</th>
                        <th class="py-1.5 px-4 font-medium w-24 text-center">Order List</th>
                        <th class="py-1.5 px-4 font-medium">Menu Name</th>
                        <th class="py-1.5 px-4 font-medium">URL Route</th>"""
content = content.replace(old_menu_header, new_menu_header)

# 4. Add OrderList column data input
old_menu_data = """<td class="py-1.5 px-4 text-center text-gray-500">{{ m.menu_id }}</td>
                        <td class="py-1.5 px-4 font-medium text-gray-800">{% if m.parent_menu %}"""
new_menu_data = """<td class="py-1.5 px-4 text-center text-gray-500">{{ m.menu_id }}</td>
                        <td class="py-1.5 px-4 text-center">
                            <form method="POST" action="" class="inline-flex">
                                {% csrf_token %}
                                <input type="hidden" name="action" value="save_menu">
                                <input type="hidden" name="menu_id" value="{{ m.menu_id }}">
                                <input type="hidden" name="menu_name" value="{{ m.menu_name }}">
                                <input type="hidden" name="url_page" value="{{ m.url_page }}">
                                <input type="hidden" name="is_active" value="{% if m.is_active %}on{% endif %}">
                                <input type="number" name="display_order" value="{{ m.display_order }}" class="w-16 border border-gray-300 rounded px-1.5 py-1 text-xs text-center focus:ring-indigo-500 focus:border-indigo-500" onchange="this.form.submit()">
                            </form>
                        </td>
                        <td class="py-1.5 px-4 font-medium text-gray-800">{% if m.parent_menu %}"""
content = content.replace(old_menu_data, new_menu_data)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
