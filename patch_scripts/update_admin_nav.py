import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# I want to add the Admin dropdown right after 'Notifications' and 'Reports' or replace the 'Go to Admin' button entirely.
# Let's replace the whole block after Reports.

old_end_nav = """            <a href="{% url 'generic_page' 'notifications' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Notifications / Reminders' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Notifications</a>
            <a href="{% url 'reports' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Reports' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>
        </nav>
        <div class="p-4 border-t border-indigo-800">
            <a href="/admin/" class="block text-center px-4 py-2 bg-indigo-600 rounded-md hover:bg-indigo-500">Go to Admin</a>
        </div>"""

new_end_nav = """            <a href="{% url 'generic_page' 'notifications' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Notifications / Reminders' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %}">Notifications</a>
            <a href="{% url 'reports' %}" class="block px-4 py-2 rounded-md {% if page_title == 'Reports' %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">Reports</a>
            
            <!-- Admin Menu -->
            <div x-data="{ open: {% if page_title == 'Admin' %}true{% else %}false{% endif %} }" class="mb-1">
                <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 rounded-md {% if page_title == 'Admin' %}bg-indigo-800 text-white{% else %}hover:bg-indigo-700{% endif %} transition-colors">
                    <span>Admin</span>
                    <i :class="open ? 'fa-solid fa-chevron-up text-xs' : 'fa-solid fa-chevron-down text-xs'"></i>
                </button>
                <div x-show="open" x-collapse class="pl-4 pr-2 py-1 space-y-1">
                    <a href="{% url 'admin_dashboard' %}?tab=dashboard" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'dashboard' or not request.GET.tab and request.resolver_match.url_name == 'admin_dashboard' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Dashboard</a>
                    <a href="{% url 'admin_dashboard' %}?tab=users" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'users' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">User Management</a>
                    <a href="{% url 'admin_dashboard' %}?tab=roles" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'roles' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Role Management</a>
                    <a href="{% url 'admin_dashboard' %}?tab=menu" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'menu' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Menu Permissions</a>
                    <a href="{% url 'admin_dashboard' %}?tab=settings" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'settings' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">System Settings</a>
                    <a href="{% url 'admin_dashboard' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == 'audit' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>
                </div>
            </div>
            
        </nav>
        <div class="p-4 border-t border-indigo-800 text-xs text-center text-indigo-300">
            Melo's Music Admin
        </div>"""

content = content.replace(old_end_nav, new_end_nav)

with open('templates/base.html', 'w') as f:
    f.write(content)
