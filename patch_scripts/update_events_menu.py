with open('templates/base.html', 'r') as f:
    content = f.read()

import re

old_menu = r'<a href="\{% url \'generic_page\' \'event_scheduling\' %\}" class="flex items-center px-6 py-3 hover:bg-indigo-700 transition-colors">\s*<i class="fa-regular fa-calendar-days w-6 text-center text-indigo-300"></i>\s*<span class="ml-3 font-medium">Event Scheduling</span>\s*</a>'

new_menu = """<div x-data="{ expanded: '{{ page_title }}' === 'Event Scheduling' }">
                <button @click="expanded = !expanded" class="w-full flex justify-between items-center px-6 py-3 hover:bg-indigo-700 transition-colors focus:outline-none">
                    <div class="flex items-center">
                        <i class="fa-regular fa-calendar-days w-6 text-center text-indigo-300"></i>
                        <span class="ml-3 font-medium">Event Scheduling</span>
                    </div>
                    <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="expanded ? 'rotate-180' : ''"></i>
                </button>
                <div x-show="expanded" x-collapse class="bg-indigo-950 px-6 py-2 space-y-1">
                    <a href="{% url 'events_dashboard' %}?tab=calendar" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Calendar View</a>
                    <a href="{% url 'events_dashboard' %}?tab=create" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Create Event</a>
                    <a href="{% url 'events_dashboard' %}?tab=upcoming" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Upcoming Events</a>
                    <a href="{% url 'events_dashboard' %}?tab=registration" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Event Registration</a>
                    <a href="{% url 'events_dashboard' %}?tab=assignments" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Teacher Assignments</a>
                    <a href="{% url 'events_dashboard' %}?tab=venue" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Venue Management</a>
                    <a href="{% url 'events_dashboard' %}?tab=attendance" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Event Attendance</a>
                    <a href="{% url 'events_dashboard' %}?tab=reports" class="block px-4 py-2 text-sm rounded-md hover:bg-indigo-700">Event Reports</a>
                </div>
            </div>"""

content = re.sub(old_menu, new_menu, content)

with open('templates/base.html', 'w') as f:
    f.write(content)
