import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update x-data
old_xdata = r'x-data="\{ tab: \'\{\{ active_tab\|default:\'list\' \}\}\', showCreateModal: \{% if active_tab == \'create\' %\}true\{% else %\}false\{% endif %\} \}"'
new_xdata = 'x-data="{ tab: \'{{ active_tab|default:\'list\' }}\', showCreateModal: {% if edit_mode %}true{% else %}false{% endif %} }"'
content = re.sub(old_xdata, new_xdata, content)

# 2. Replace all instances of `selected_event and active_tab == 'create'` with `selected_event and edit_mode`
content = content.replace("selected_event and active_tab == 'create'", "selected_event and edit_mode")

# 3. Replace all instances of `active_tab == 'create' && selected_event` in Alpine with `edit_mode`
# Ah, the Alpine text used tab === 'create'.
content = content.replace("tab === 'create' && selected_event ? 'Edit Event' : 'Add Event'", "'{{ edit_mode|yesno:\"Edit Event,Add Event\" }}'")

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
