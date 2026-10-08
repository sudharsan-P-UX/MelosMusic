import re

with open('templates/base.html', 'r') as f:
    content = f.read()

old_admin_menu = """            <!-- Admin Menu -->
            <div x-data="{ open: {% if page_title == 'Admin' %}true{% else %}false{% endif %} }" class="mb-1">"""

new_admin_menu = """            <!-- Admin Menu -->
            {% if user_perms.Admin.view %}
            <div x-data="{ open: {% if page_title == 'Admin' %}true{% else %}false{% endif %} }" class="mb-1">"""

content = content.replace(old_admin_menu, new_admin_menu)


old_admin_end = """                    <a href="{% url 'admin_dashboard' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'audit' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>
                </div>
            </div>"""

new_admin_end = """                    <a href="{% url 'admin_dashboard' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'audit' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>
                </div>
            </div>
            {% endif %}"""

content = content.replace(old_admin_end, new_admin_end)

with open('templates/base.html', 'w') as f:
    f.write(content)
