import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Title bar changes
old_title_bar = r'<div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">.*?</div>\s*</div>\s*<div class="p-6">'

new_title_bar = """<div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 class="text-xl font-semibold text-gray-800" x-text="{
            'calendar': 'Event Calendar',
            'create': 'Create / Edit Event',
            'upcoming': 'Event List',
            'list': 'Event List',
            'details': 'Event Details',
            'registration': 'Event Participant Registration',
            'assignments': 'Teacher Assignments',
            'venue': 'Venue Management',
            'attendance': 'Event Attendance',
            'reports': 'Event Reports'
        }[tab] || 'Event Scheduling'"></h2>
        
        <div class="flex space-x-3">
            <button x-show="tab === 'registration'" class="bg-[#5c4baf] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Participant
            </button>
            <button x-show="['list', 'upcoming', 'calendar'].includes(tab)" @click="tab = 'create'" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Event
            </button>
            <div x-show="tab === 'details'" class="flex space-x-2">
                <button @click="tab = 'create'" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                    <i class="fa-solid fa-pen mr-1.5"></i> Edit
                </button>
                <button class="bg-red-500 hover:bg-red-600 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                    <i class="fa-solid fa-trash-can mr-1.5"></i> Delete
                </button>
            </div>
            <div x-show="['details', 'create'].includes(tab)">
                <button @click="tab = 'list'" class="text-indigo-600 hover:underline flex items-center text-xs mt-1 mr-4">
                    <i class="fa-solid fa-arrow-left mr-1"></i> Back to List
                </button>
            </div>
        </div>
    </div>
    
    <div class="p-6">"""

content = re.sub(old_title_bar, new_title_bar, content, flags=re.DOTALL)

# 2. Upcoming Events -> Event List UI
old_upcoming = r'<!-- 6\. Upcoming Events -->.*?</div>\s*</div>\s*</div>'

new_event_list = """<!-- Event List -->
        <div x-show="['upcoming', 'list'].includes(tab)" x-transition style="display: none;">
            
            <div class="flex flex-wrap gap-4 items-end mb-6">
                <div class="flex-1 min-w-[200px]">
                    <input type="text" placeholder="Search event name..." class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                </div>
                <div class="w-48">
                    <label class="block text-xs text-gray-500 mb-1">Event Type</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none bg-white">
                        <option>All</option>
                    </select>
                </div>
                <div class="w-48">
                    <label class="block text-xs text-gray-500 mb-1">Status</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none bg-white">
                        <option>All</option>
                    </select>
                </div>
                <div class="w-40">
                    <label class="block text-xs text-gray-500 mb-1">From Date</label>
                    <input type="date" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none text-gray-500">
                </div>
                <div class="w-40">
                    <label class="block text-xs text-gray-500 mb-1">To Date</label>
                    <input type="date" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none text-gray-500">
                </div>
                <div class="flex space-x-2">
                    <button class="bg-[#4f46e5] text-white px-5 py-2 rounded text-sm shadow-sm flex items-center hover:bg-indigo-700">
                        <i class="fa-solid fa-filter mr-1.5"></i> Filter
                    </button>
                    <button class="border border-red-200 text-red-500 px-5 py-2 rounded text-sm hover:bg-red-50">
                        Reset
                    </button>
                </div>
            </div>

            <div class="border border-gray-200 rounded bg-white shadow-sm overflow-hidden">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="border-b border-gray-200 text-gray-600 bg-gray-50/50">
                            <th class="py-3 px-4 font-semibold w-12 text-center">#</th>
                            <th class="py-3 px-4 font-semibold">Event Name</th>
                            <th class="py-3 px-4 font-semibold">Event Type</th>
                            <th class="py-3 px-4 font-semibold">Event Date</th>
                            <th class="py-3 px-4 font-semibold">Start Time</th>
                            <th class="py-3 px-4 font-semibold">End Time</th>
                            <th class="py-3 px-4 font-semibold">Venue</th>
                            <th class="py-3 px-4 font-semibold text-center">Status</th>
                            <th class="py-3 px-4 font-semibold text-center w-28">Action</th>
                        </tr>
                    </thead>
                    <tbody class="text-gray-700">
                        {% for ev in events %}
                        <tr class="border-b border-gray-100 hover:bg-gray-50">
                            <td class="py-3 px-4 text-center">{{ forloop.counter }}</td>
                            <td class="py-3 px-4 font-medium text-gray-800">{{ ev.event_name }}</td>
                            <td class="py-3 px-4">{{ ev.event_type }}</td>
                            <td class="py-3 px-4">{{ ev.event_date|date:"d/m/Y" }}</td>
                            <td class="py-3 px-4">{{ ev.start_time|time:"h:i A" }}</td>
                            <td class="py-3 px-4">{{ ev.end_time|time:"h:i A" }}</td>
                            <td class="py-3 px-4 text-gray-600">{% if ev.venue %}{{ ev.venue.venue_name }}{% else %}TBA{% endif %}</td>
                            <td class="py-3 px-4 text-center">
                                {% if ev.status == 1 %}<span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-[10px] font-medium">Upcoming</span>
                                {% elif ev.status == 2 %}<span class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full text-[10px] font-medium">Completed</span>
                                {% else %}<span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-[10px] font-medium">Cancelled</span>{% endif %}
                            </td>
                            <td class="py-3 px-4 text-center">
                                <div class="flex items-center justify-center space-x-2">
                                    <a href="?tab=details&event_id={{ ev.event_id }}" class="w-7 h-7 rounded-full bg-indigo-50 text-indigo-500 flex items-center justify-center hover:bg-indigo-100 transition"><i class="fa-regular fa-eye"></i></a>
                                    <a href="?tab=create&event_id={{ ev.event_id }}" class="w-7 h-7 rounded-full bg-blue-50 text-blue-500 flex items-center justify-center hover:bg-blue-100 transition"><i class="fa-solid fa-pen text-[10px]"></i></a>
                                    <button class="w-7 h-7 rounded-full bg-red-50 text-red-500 flex items-center justify-center hover:bg-red-100 transition"><i class="fa-solid fa-trash-can text-[10px]"></i></button>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr><td colspan="9" class="text-center py-8 text-gray-400">No events found. Click 'Add Event' to create one.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div class="px-4 py-3 border-t border-gray-200 flex justify-between items-center text-xs text-gray-500 bg-white">
                    <div>Showing 1 to {{ events|length }} of {{ events|length }} entries</div>
                    <div class="flex border border-gray-300 rounded overflow-hidden">
                        <button class="px-3 py-1.5 bg-white hover:bg-gray-50 border-r border-gray-300">Previous</button>
                        <button class="px-3 py-1.5 bg-[#4f46e5] text-white">1</button>
                        <button class="px-3 py-1.5 bg-white hover:bg-gray-50 border-l border-gray-300">Next</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 7. View Event Details -->
        <div x-show="tab === 'details'" x-transition style="display: none;">
            {% if selected_event %}
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Left side -->
                <div class="space-y-6">
                    <div class="border border-gray-200 rounded p-6 shadow-sm">
                        <h3 class="font-medium text-gray-800 mb-4 pb-2 border-b border-gray-100">Event Information</h3>
                        <div class="space-y-4 text-sm">
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Event Name</div><div class="flex-1">: <span class="text-gray-800 font-medium ml-2">{{ selected_event.event_name }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Event Type</div><div class="flex-1">: <span class="text-gray-700 ml-2">{{ selected_event.event_type }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Description</div><div class="flex-1">: <span class="text-gray-600 ml-2">{{ selected_event.description|default:"-" }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Event Date</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.event_date|date:"d/m/Y (l)" }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Start Time</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.start_time|time:"h:i A" }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">End Time</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.end_time|time:"h:i A" }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Venue</div><div class="flex-1">: <span class="text-gray-800 ml-2">{% if selected_event.venue %}{{ selected_event.venue.venue_name }}{% else %}TBA{% endif %}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Status</div><div class="flex-1">: <span class="text-gray-800 font-medium ml-2">{% if selected_event.status == 1 %}Upcoming{% elif selected_event.status == 2 %}Completed{% else %}Cancelled{% endif %}</span></div></div>
                        </div>
                    </div>
                    
                    <div class="border border-gray-200 rounded p-6 shadow-sm">
                        <h3 class="font-medium text-gray-800 mb-4 pb-2 border-b border-gray-100">Additional Information</h3>
                        <div class="grid grid-cols-2 gap-y-4 text-sm">
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Organizer</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.organizer|default:"-" }}</span></div></div>
                            <div class="flex"><div class="w-36 font-medium text-gray-600">Registration Period</div><div class="flex-1">: <span class="text-gray-800 ml-2">{% if selected_event.registration_start_date %}{{ selected_event.registration_start_date|date:"d/m/Y" }} - {{ selected_event.registration_end_date|date:"d/m/Y" }}{% else %}-{% endif %}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Contact Person</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.contact_person|default:"-" }}</span></div></div>
                            <div class="flex"><div class="w-36 font-medium text-gray-600">Max Participants</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.max_participants|default:"-" }}</span></div></div>
                            <div class="flex"><div class="w-32 font-medium text-gray-600">Contact Phone</div><div class="flex-1">: <span class="text-gray-800 ml-2">{{ selected_event.contact_phone|default:"-" }}</span></div></div>
                        </div>
                    </div>
                </div>
                
                <!-- Right side -->
                <div>
                    <div class="border border-gray-200 rounded p-6 shadow-sm h-full">
                        <h3 class="font-medium text-gray-800 mb-4 pb-2 border-b border-gray-100">Event Banner / Image</h3>
                        <div class="rounded-lg overflow-hidden border border-gray-200 shadow-inner bg-gray-50">
                            <!-- Placeholder image, simulating uploaded banner -->
                            <div class="aspect-video bg-gradient-to-br from-indigo-900 to-purple-800 flex items-center justify-center relative">
                                <i class="fa-solid fa-music text-6xl text-white/30"></i>
                                <div class="absolute bottom-4 left-4 right-4 flex justify-between items-end">
                                    <div class="text-white">
                                        <div class="text-lg font-bold drop-shadow-md">{{ selected_event.event_name }}</div>
                                        <div class="text-xs opacity-90">{{ selected_event.event_date|date:"d M Y" }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="text-center py-10 text-gray-500">No event selected. <a href="?tab=list" class="text-indigo-600 underline">Back to List</a></div>
            {% endif %}
        </div>

    </div>
</div>
"""

content = re.sub(old_upcoming, new_event_list, content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
