import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# Replace the Menu name cell in the Role Matrix
old_matrix_td = '<td class="py-1.5 px-4 font-medium text-gray-800"><i class="fa-solid fa-bars text-gray-300 mr-2 text-xs"></i> {{ menu.menu_name }}</td>'
new_matrix_td = '<td class="py-1.5 px-4 font-medium text-gray-800">{% if menu.parent_menu %}<i class="fa-solid fa-level-up-alt fa-rotate-90 text-gray-300 ml-4 mr-2 text-xs"></i>{% else %}<i class="fa-solid fa-bars text-gray-300 mr-2 text-xs"></i>{% endif %} {{ menu.menu_name }}</td>'

content = content.replace(old_matrix_td, new_matrix_td)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
