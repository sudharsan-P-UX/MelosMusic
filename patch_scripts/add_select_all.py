import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update the 'Menu' table header to include the Master Select All checkbox
old_menu_th = '<th class="py-1.5 px-4 font-semibold w-1/3">Menu</th>'
new_menu_th = """<th class="py-1.5 px-4 font-semibold w-1/3">
                                    <label class="flex items-center cursor-pointer">
                                        <input type="checkbox" onchange="document.querySelectorAll('.perm-chk').forEach(c => c.checked = this.checked)" class="mr-2 rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300 cursor-pointer">
                                        Select All
                                    </label>
                                </th>"""
content = content.replace(old_menu_th, new_menu_th)

# 2. Add the 'perm-chk' class to all checkboxes in the matrix
old_chk_classes = 'class="rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300"'
new_chk_classes = 'class="perm-chk rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300 cursor-pointer"'
# We must only replace inside the Role Matrix. Since the checkboxes there are identical, we can safely replace.
# Actually, wait, let's just make sure we only replace inside the matrix.
# The Role Matrix has `name="view_{{ menu.menu_id }}"`, etc.
for perm in ['view', 'add', 'edit', 'delete', 'export']:
    old_input = f'name="{perm}_{{{{ menu.menu_id }}}}" {{% for k,v in role_access_map.items %}}{{% if k == menu.menu_id and v.{perm}_access %}}checked{{% endif %}}{{% endfor %}} {old_chk_classes}'
    new_input = f'name="{perm}_{{{{ menu.menu_id }}}}" {{% for k,v in role_access_map.items %}}{{% if k == menu.menu_id and v.{perm}_access %}}checked{{% endif %}}{{% endfor %}} {new_chk_classes}'
    content = content.replace(old_input, new_input)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
