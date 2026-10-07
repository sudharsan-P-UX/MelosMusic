import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# Fix hidden event_id input
content = content.replace(
    "{% if selected_event and tab == 'create' %}",
    "{% if selected_event and edit_mode %}"
)

# Fix event type selects
content = content.replace("{% if selected_event.event_type == 'Performance' %}", "{% if selected_event and edit_mode and selected_event.event_type == 'Performance' %}")
content = content.replace("{% if selected_event.event_type == 'Workshop' %}", "{% if selected_event and edit_mode and selected_event.event_type == 'Workshop' %}")
content = content.replace("{% if selected_event.event_type == 'Competition' %}", "{% if selected_event and edit_mode and selected_event.event_type == 'Competition' %}")
content = content.replace("{% if selected_event.event_type == 'Meeting' %}", "{% if selected_event and edit_mode and selected_event.event_type == 'Meeting' %}")

# Fix venue select
content = content.replace("{% if selected_event and selected_event.venue_id == venue.venue_id %}", "{% if selected_event and edit_mode and selected_event.venue_id == venue.venue_id %}")
content = content.replace("{% if selected_event and not selected_event.venue %}", "{% if selected_event and edit_mode and not selected_event.venue %}")

# Fix status select
content = content.replace("{% if selected_event and selected_event.status == 1 %}", "{% if selected_event and edit_mode and selected_event.status == 1 %}")
content = content.replace("{% if selected_event and selected_event.status == 2 %}", "{% if selected_event and edit_mode and selected_event.status == 2 %}")
content = content.replace("{% if selected_event and selected_event.status == 3 %}", "{% if selected_event and edit_mode and selected_event.status == 3 %}")

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
