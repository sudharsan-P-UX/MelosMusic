import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

old_create = r'<form method="POST" action="{% url \'create_event\' %}" class="grid grid-cols-2 gap-8 max-w-3xl">.*?</form>'

new_create = """<form method="POST" action="{% url 'create_event' %}" class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl bg-white p-6 rounded shadow-sm border border-gray-100">
                {% csrf_token %}
                {% if selected_event and tab == 'create' %}
                <input type="hidden" name="event_id" value="{{ selected_event.event_id }}">
                {% endif %}
                <div class="space-y-5">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Name <span class="text-red-500">*</span></label>
                        <input type="text" name="event_name" value="{% if selected_event and tab == 'create' %}{{ selected_event.event_name }}{% endif %}" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Type <span class="text-red-500">*</span></label>
                        <select name="event_type" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                            <option value="">Select Type...</option>
                            <option value="Performance" {% if selected_event.event_type == 'Performance' %}selected{% endif %}>Performance</option>
                            <option value="Workshop" {% if selected_event.event_type == 'Workshop' %}selected{% endif %}>Workshop</option>
                            <option value="Competition" {% if selected_event.event_type == 'Competition' %}selected{% endif %}>Competition</option>
                            <option value="Meeting" {% if selected_event.event_type == 'Meeting' %}selected{% endif %}>Meeting</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Date <span class="text-red-500">*</span></label>
                        <input type="date" name="event_date" value="{% if selected_event and tab == 'create' %}{{ selected_event.event_date|date:'Y-m-d' }}{% endif %}" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 text-gray-600">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Start Time <span class="text-red-500">*</span></label>
                            <input type="time" name="start_time" value="{% if selected_event and tab == 'create' %}{{ selected_event.start_time|time:'H:i' }}{% endif %}" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">End Time <span class="text-red-500">*</span></label>
                            <input type="time" name="end_time" value="{% if selected_event and tab == 'create' %}{{ selected_event.end_time|time:'H:i' }}{% endif %}" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Venue <span class="text-red-500">*</span></label>
                        <select name="venue_id" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                            <option value="">Select Venue...</option>
                            {% for venue in venues %}
                            <option value="{{ venue.venue_id }}" {% if selected_event and selected_event.venue_id == venue.venue_id %}selected{% endif %}>{{ venue.venue_name }}</option>
                            {% endfor %}
                            <option value="0" {% if selected_event and not selected_event.venue %}selected{% endif %}>TBA / Online</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Status <span class="text-red-500">*</span></label>
                        <select name="status" required class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                            <option value="1" {% if selected_event and selected_event.status == 1 %}selected{% endif %}>Upcoming</option>
                            <option value="2" {% if selected_event and selected_event.status == 2 %}selected{% endif %}>Completed</option>
                            <option value="3" {% if selected_event and selected_event.status == 3 %}selected{% endif %}>Cancelled</option>
                        </select>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4 border-t border-gray-100 pt-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Registration Start Date <span class="text-red-500">*</span></label>
                            <input type="date" name="registration_start_date" value="{% if selected_event and tab == 'create' %}{{ selected_event.registration_start_date|date:'Y-m-d' }}{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Registration End Date <span class="text-red-500">*</span></label>
                            <input type="date" name="registration_end_date" value="{% if selected_event and tab == 'create' %}{{ selected_event.registration_end_date|date:'Y-m-d' }}{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 text-gray-600">
                        </div>
                    </div>
                </div>
                
                <div class="space-y-5">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Description <span class="text-red-500">*</span></label>
                        <textarea name="description" rows="3" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">{% if selected_event and tab == 'create' %}{{ selected_event.description }}{% endif %}</textarea>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 mb-1">Event Banner / Image</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg h-32 flex flex-col items-center justify-center bg-gray-50 relative overflow-hidden">
                            {% if selected_event and tab == 'create' %}
                            <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 to-purple-800 opacity-60"></div>
                            <button type="button" class="relative z-10 bg-white/90 border border-gray-300 px-4 py-1.5 rounded text-indigo-600 hover:bg-white text-xs shadow-sm font-medium">Change Image</button>
                            <span class="relative z-10 text-[10px] text-white mt-1 font-medium">JPG, PNG (Max 2MB)</span>
                            {% else %}
                            <i class="fa-solid fa-image text-3xl text-gray-300 mb-2"></i>
                            <button type="button" class="border border-gray-300 px-4 py-1.5 rounded text-gray-600 bg-white hover:bg-gray-100 text-xs shadow-sm mb-1">Choose File</button>
                            <span class="text-[10px] text-gray-400">JPG, PNG (Max 2MB)</span>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="border-t border-gray-100 pt-4 space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Organizer <span class="text-red-500">*</span></label>
                            <input type="text" name="organizer" value="{% if selected_event and tab == 'create' %}{{ selected_event.organizer|default:'' }}{% else %}Melo's Music School{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Contact Person <span class="text-red-500">*</span></label>
                                <input type="text" name="contact_person" value="{% if selected_event and tab == 'create' %}{{ selected_event.contact_person|default:'' }}{% else %}{{ user.first_name }}{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Contact Phone <span class="text-red-500">*</span></label>
                                <input type="text" name="contact_phone" value="{% if selected_event and tab == 'create' %}{{ selected_event.contact_phone|default:'' }}{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                            </div>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Max Participants <span class="text-red-500">*</span></label>
                            <input type="number" name="max_participants" value="{% if selected_event and tab == 'create' %}{{ selected_event.max_participants|default:'' }}{% endif %}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                        </div>
                    </div>
                    
                    <div class="flex justify-end space-x-3 pt-6 border-t border-gray-100 mt-6">
                        <button type="button" @click="tab = 'list'" class="border border-gray-300 text-gray-600 px-6 py-2 rounded text-sm font-medium hover:bg-gray-50 transition">Cancel</button>
                        <button type="submit" class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">{% if selected_event and tab == 'create' %}Save Changes{% else %}Add Event{% endif %}</button>
                    </div>
                </div>
            </form>"""

content = re.sub(old_create, new_create, content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
