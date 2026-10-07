import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update x-data
old_xdata = """<div class="bg-white rounded min-h-screen font-sans text-sm" x-data="{ tab: '{{ active_tab|default:'list' }}', showCreateModal: {% if edit_mode %}true{% else %}false{% endif %} }">"""
new_xdata = """<div class="bg-white rounded min-h-screen font-sans text-sm" x-data="{ tab: '{{ active_tab|default:'list' }}', showCreateModal: {% if edit_mode %}true{% else %}false{% endif %}, showVenueModal: false }">"""
content = content.replace(old_xdata, new_xdata)

# 2. Add button in header
old_buttons = """<button x-show="['list', 'upcoming', 'calendar'].includes(tab)" @click="showCreateModal = true" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Event
            </button>"""
new_buttons = """<button x-show="['list', 'upcoming', 'calendar'].includes(tab)" @click="showCreateModal = true" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Event
            </button>
            <button x-show="tab === 'venue'" @click="showVenueModal = true" class="bg-[#4f46e5] hover:bg-indigo-700 text-white px-4 py-1.5 rounded shadow-sm flex items-center text-xs transition">
                <i class="fa-solid fa-plus mr-1.5"></i> Add Venue
            </button>"""
content = content.replace(old_buttons, new_buttons)


# 3. Add Venue tab content right before Event Attendance
old_attendance_marker = """<!-- 4. Event Attendance -->
        <div x-show="tab === 'attendance'" x-transition style="display: none;">"""

venue_content = """<!-- Venue Management -->
        <div x-show="tab === 'venue'" x-transition style="display: none;">
            <table class="w-full text-left border-collapse text-sm border border-gray-200 rounded overflow-hidden">
                <thead>
                    <tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-3 px-4 font-medium w-16 text-center">#</th>
                        <th class="py-3 px-4 font-medium">Venue Name</th>
                        <th class="py-3 px-4 font-medium">Capacity</th>
                        <th class="py-3 px-4 font-medium">Address</th>
                        <th class="py-3 px-4 font-medium text-center">Actions</th>
                    </tr>
                </thead>
                <tbody class="text-gray-700">
                    {% for venue in venues %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="py-3 px-4 text-center">{{ forloop.counter }}</td>
                        <td class="py-3 px-4 font-medium text-gray-800">{{ venue.venue_name }}</td>
                        <td class="py-3 px-4 text-gray-600">{{ venue.capacity|default:"-" }}</td>
                        <td class="py-3 px-4 text-gray-500">{{ venue.address|default:"-" }}</td>
                        <td class="py-3 px-4 text-center space-x-2">
                            <button class="text-indigo-400 hover:text-indigo-600 bg-indigo-50 hover:bg-indigo-100 p-1.5 rounded transition"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 p-1.5 rounded transition"><i class="fa-solid fa-trash-can"></i></button>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="py-8 text-center text-gray-500">No venues found. Create one to get started.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- 4. Event Attendance -->
        <div x-show="tab === 'attendance'" x-transition style="display: none;">"""

content = content.replace(old_attendance_marker, venue_content)


# 4. Add Venue Modal at the end of the file, just before the closing </div> of x-data
old_end = """<!-- Toast Messages -->"""

venue_modal = """<!-- Add Venue Modal -->
        <div x-show="showVenueModal" style="display: none;" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm transition-opacity" @click="showVenueModal = false">
            <form method="POST" action="{% url 'events_dashboard' %}" class="bg-white rounded shadow-lg max-w-md w-full flex flex-col" @click.stop autocomplete="off">
                {% csrf_token %}
                <input type="hidden" name="action" value="add_venue">
                
                <div class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center rounded-t">
                    <h3 class="text-lg font-medium text-gray-800">Add Venue</h3>
                    <button type="button" @click="showVenueModal = false" class="text-gray-400 hover:text-gray-600 transition">
                        <i class="fa-solid fa-xmark text-lg"></i>
                    </button>
                </div>
                
                <div class="p-6 space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Venue Name <span class="text-red-500">*</span></label>
                        <input type="text" name="venue_name" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
                        <input type="number" name="capacity" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Address / Location Details</label>
                        <textarea name="address" rows="3" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500"></textarea>
                    </div>
                </div>
                
                <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end space-x-3 rounded-b">
                    <button type="button" @click="showVenueModal = false" class="border border-gray-300 bg-white text-gray-700 px-4 py-2 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>
                    <button type="submit" class="bg-[#4f46e5] text-white px-4 py-2 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">Save Venue</button>
                </div>
            </form>
        </div>
        
        <!-- Toast Messages -->"""

content = content.replace(old_end, venue_modal)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
