import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

# 1. Update the Create Event form
old_create_form = r'<div x-show="tab === \'create\'" x-transition style="display: none;">\s*<div class="grid grid-cols-2 gap-8 max-w-3xl">.*?</div>\s*</div>'

new_create_form = """<div x-show="tab === 'create'" x-transition style="display: none;">
            <form method="POST" action="{% url 'create_event' %}" class="grid grid-cols-2 gap-8 max-w-3xl">
                {% csrf_token %}
                <div class="space-y-5">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Name <span class="text-red-500">*</span></label>
                        <input type="text" name="event_name" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Type <span class="text-red-500">*</span></label>
                        <select name="event_type" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 bg-white">
                            <option value="">Select Type...</option>
                            <option value="Performance">Performance</option>
                            <option value="Workshop">Workshop</option>
                            <option value="Competition">Competition</option>
                            <option value="Meeting">Meeting</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Date <span class="text-red-500">*</span></label>
                        <input type="date" name="event_date" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 text-gray-600">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Start Time <span class="text-red-500">*</span></label>
                            <input type="time" name="start_time" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">End Time <span class="text-red-500">*</span></label>
                            <input type="time" name="end_time" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Venue <span class="text-red-500">*</span></label>
                        <select name="venue_id" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 bg-white">
                            <option value="">Select Venue...</option>
                            {% for venue in venues %}
                            <option value="{{ venue.venue_id }}">{{ venue.venue_name }}</option>
                            {% endfor %}
                            <option value="0">TBA / Online</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Status <span class="text-red-500">*</span></label>
                        <select name="status" required class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500 bg-white">
                            <option value="1">Upcoming</option>
                            <option value="2">Completed</option>
                            <option value="3">Cancelled</option>
                        </select>
                    </div>
                </div>
                
                <div class="space-y-5">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Description</label>
                        <textarea name="description" rows="3" class="w-full border border-gray-300 rounded px-3 py-2 outline-none focus:border-indigo-500"></textarea>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Banner / Image</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg h-40 flex flex-col items-center justify-center bg-gray-50">
                            <i class="fa-solid fa-image text-4xl text-gray-300 mb-2"></i>
                            <button type="button" class="border border-gray-300 px-4 py-1.5 rounded text-gray-600 bg-white hover:bg-gray-100 text-xs shadow-sm mb-2">Choose File</button>
                            <span class="text-[10px] text-gray-400">JPG, PNG (Max 2MB)</span>
                        </div>
                    </div>
                    
                    <div class="flex justify-end space-x-3 pt-10">
                        <button type="button" @click="tab = 'calendar'" class="border border-gray-300 text-gray-600 px-6 py-2 rounded hover:bg-gray-50 transition">Cancel</button>
                        <button type="submit" class="bg-[#5c4baf] text-white px-6 py-2 rounded hover:bg-indigo-700 shadow-sm transition">Add Event</button>
                    </div>
                </div>
            </form>
        </div>"""

content = re.sub(old_create_form, new_create_form, content, flags=re.DOTALL)

# 2. Update the Upcoming Events List
old_upcoming_list = r'<tbody class="text-gray-700">.*?</tbody>'

new_upcoming_list = """<tbody class="text-gray-700">
                            {% for ev in events %}
                            <tr class="border-b border-gray-100 hover:bg-gray-50">
                                <td class="py-3 font-medium text-gray-800">{{ ev.event_name }}</td>
                                <td class="py-3">{{ ev.event_date|date:"d/m/Y" }}</td>
                                <td class="py-3">{{ ev.start_time|time:"h:i A" }}</td>
                                <td class="py-3 text-gray-500">{% if ev.venue %}{{ ev.venue.venue_name }}{% else %}TBA{% endif %}</td>
                                <td class="py-3 text-center">0</td>
                                <td class="py-3 text-center">
                                    {% if ev.status == 1 %}<span class="text-gray-500">Upcoming</span>
                                    {% elif ev.status == 2 %}<span class="text-green-500">Completed</span>
                                    {% else %}<span class="text-red-500">Cancelled</span>{% endif %}
                                </td>
                            </tr>
                            {% empty %}
                            <tr><td colspan="6" class="text-center py-6 text-gray-400">No events found.</td></tr>
                            {% endfor %}
                        </tbody>"""

# Because there are multiple tbodys, we need to be precise. 
# Let's use a simpler approach. I'll split by "Upcoming Events List" and then replace the first tbody after it.
parts = content.split('Upcoming Events List</h4>')
if len(parts) > 1:
    sub_parts = re.split(r'<tbody class="text-gray-700">.*?</tbody>', parts[1], maxsplit=1, flags=re.DOTALL)
    if len(sub_parts) > 1:
        parts[1] = sub_parts[0] + new_upcoming_list + sub_parts[1]
    content = 'Upcoming Events List</h4>'.join(parts)


with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)

