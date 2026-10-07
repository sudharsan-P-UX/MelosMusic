import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Replace the sub-menu items with conditional classes
submenus = [
    ('upcoming', 'list', 'Event List'),
    ('registration', 'registration', 'Event Registration'),
    ('assignments', 'assignments', 'Teacher Assignments'),
    ('venue', 'venue', 'Venue Management'),
    ('attendance', 'attendance', 'Event Attendance'),
    ('reports', 'reports', 'Event Reports')
]

for old_tab, new_tab, label in submenus:
    # Handle the 'upcoming' -> 'list' or 'upcoming' case
    if old_tab == 'upcoming':
        old_link = f'<a href="{{% url \'events_dashboard\' %}}?tab={old_tab}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">{label}</a>'
        new_link = f'<a href="{{% url \'events_dashboard\' %}}?tab={old_tab}" class="block px-4 py-2 text-sm rounded-md {{% if active_tab == \'{old_tab}\' or active_tab == \'list\' %}}bg-indigo-600 text-white font-medium{{% else %}}hover:bg-indigo-700{{% endif %}}">{label}</a>'
    else:
        old_link = f'<a href="{{% url \'events_dashboard\' %}}?tab={old_tab}" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">{label}</a>'
        new_link = f'<a href="{{% url \'events_dashboard\' %}}?tab={old_tab}" class="block px-4 py-2 text-sm rounded-md {{% if active_tab == \'{old_tab}\' %}}bg-indigo-600 text-white font-medium{{% else %}}hover:bg-indigo-700{{% endif %}}">{label}</a>'
    
    content = content.replace(old_link, new_link)

with open('templates/base.html', 'w') as f:
    f.write(content)
