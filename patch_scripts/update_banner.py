import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

old_banner = r'<!-- Summary Header -->\s*<div class="flex space-x-12 mb-8 bg-gray-50 p-4 rounded border border-gray-200">.*?</div>\s*</div>\s*<!-- Filters -->'

new_banner = """<!-- Summary Header -->
            <div class="flex space-x-12 mb-8 bg-gray-50 p-4 rounded border border-gray-200">
                {% if selected_event %}
                <div>
                    <div class="text-xs text-gray-500 mb-1">Event Name</div>
                    <div class="font-medium text-gray-800">{{ selected_event.event_name }}</div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">Event Date</div>
                    <div class="font-medium text-gray-800">{{ selected_event.event_date|date:"d/m/Y" }}</div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">Time</div>
                    <div class="font-medium text-gray-800">{{ selected_event.start_time|time:"h:i A" }} - {{ selected_event.end_time|time:"h:i A" }}</div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">Venue</div>
                    <div class="font-medium text-gray-800">{% if selected_event.venue %}{{ selected_event.venue.venue_name }}{% else %}TBA{% endif %}</div>
                </div>
                {% else %}
                <div class="text-gray-500">No event selected or available. Please create an event first.</div>
                {% endif %}
            </div>
            
            <!-- Filters -->"""

content = re.sub(old_banner, new_banner, content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
