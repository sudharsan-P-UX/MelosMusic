import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Replace previous get_item hacks with dot notation fallback logic if they were applied
# First reset back to clean (since wire_sidebar was already written but not executed, wait, I haven't executed it!)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=dashboard" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'dashboard\' or not request.GET.tab and request.resolver_match.url_name == \'admin_dashboard\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Dashboard</a>',
    '{% if user_perms.Admin_Dashboard.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=dashboard" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'dashboard\' or not request.GET.tab and request.resolver_match.url_name == \'admin_dashboard\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Dashboard</a>{% endif %}'
)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=users" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'users\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">User Management</a>',
    '{% if user_perms.User_Management.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=users" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'users\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">User Management</a>{% endif %}'
)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=roles" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'roles\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Role Management</a>',
    '{% if user_perms.Role_Management.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=roles" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'roles\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Role Management</a>{% endif %}'
)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=menu" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'menu\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Menu Permissions</a>',
    '{% if user_perms.Menu_Permissions.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=menu" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'menu\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Menu Permissions</a>{% endif %}'
)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=settings" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'settings\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">System Settings</a>',
    '{% if user_perms.System_Settings.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=settings" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'settings\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">System Settings</a>{% endif %}'
)

content = content.replace(
    '<a href="{% url \'admin_dashboard\' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'audit\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>',
    '{% if user_perms.Audit_Logs.view or user_perms.Admin.view %}<a href="{% url \'admin_dashboard\' %}?tab=audit" class="block px-4 py-1.5 rounded-md text-sm {% if request.GET.tab == \'audit\' %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">Audit Logs</a>{% endif %}'
)

with open('templates/base.html', 'w') as f:
    f.write(content)
