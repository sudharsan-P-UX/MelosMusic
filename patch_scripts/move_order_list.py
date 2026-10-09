import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Replace the table header
old_thead = """<tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-1.5 px-4 font-medium w-16 text-center">ID</th>
                        <th class="py-1.5 px-4 font-medium w-24 text-center">Order List</th>
                        <th class="py-1.5 px-4 font-medium">Menu Name</th>
                        <th class="py-1.5 px-4 font-medium">URL Route</th>
                        <th class="py-1.5 px-4 font-medium text-center">Status</th>
                        <th class="py-1.5 px-4 font-medium text-center">Actions</th>
                    </tr>"""

new_thead = """<tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-1.5 px-4 font-medium">Menu Name</th>
                        <th class="py-1.5 px-4 font-medium">URL Route</th>
                        <th class="py-1.5 px-4 font-medium text-center">Status</th>
                        <th class="py-1.5 px-4 font-medium text-center">Actions</th>
                        <th class="py-1.5 px-4 font-medium w-24 text-center">Order List</th>
                    </tr>"""

content = content.replace(old_thead, new_thead)

# Replace the table row data (we need to carefully extract the pieces)
# The row structure is currently:
# 1. ID
# 2. Order List form
# 3. Menu Name
# 4. URL
# 5. Status
# 6. Actions

# Since it spans multiple lines, it's easier to just rebuild the tr contents with a regex
row_pattern = re.compile(
    r'(<tr class="border-b border-gray-100 hover:bg-gray-50">)\s*'
    r'<td class="py-1\.5 px-4 text-center text-gray-500">{{ m\.menu_id }}</td>\s*'
    r'(<td class="py-1\.5 px-4 text-center">\s*<form method="POST" action="" class="inline-flex">.*?</form>\s*</td>)\s*'
    r'(<td class="py-1\.5 px-4 font-medium text-gray-800">.*?</td>)\s*'
    r'(<td class="py-1\.5 px-4 text-gray-500 font-mono text-xs">{{ m\.url_page }}</td>)\s*'
    r'(<td class="py-1\.5 px-4 text-center">\s*{% if m\.is_active %}.*?</td>)\s*'
    r'(<td class="py-1\.5 px-4 text-center space-x-2">.*?</td>)',
    re.DOTALL
)

def row_replacement(match):
    tr_start = match.group(1)
    order_list_td = match.group(2)
    menu_name_td = match.group(3)
    url_td = match.group(4)
    status_td = match.group(5)
    actions_td = match.group(6)
    
    return f"{tr_start}\n                        {menu_name_td}\n                        {url_td}\n                        {status_td}\n                        {actions_td}\n                        {order_list_td}"

content = row_pattern.sub(row_replacement, content)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
