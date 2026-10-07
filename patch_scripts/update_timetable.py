with open('templates/website/timetable.html', 'r') as f:
    content = f.read()

old_loop = """            {% for day in days %}
            <div class="flex flex-col">
                <div class="bg-indigo-100 text-indigo-800 font-bold text-center py-2 rounded-t-md border-b-2 border-indigo-200 uppercase text-xs tracking-wider">
                    {{ day }}
                </div>
                <div class="bg-gray-50 border border-gray-200 border-t-0 rounded-b-md flex-1 p-2 space-y-3 min-h-[400px]">
                    {% for slot in schedule|dictsort:day %}
                    <!-- We iterate through the dictionary -->
                    {% endfor %}
                    <!-- Since dict lookup in Django templates is tricky without a custom filter, let's just pass them properly or iterate -->
                </div>
            </div>
            {% endfor %}"""
            
new_loop = """            {% for day, day_slots in schedule_data %}
            <div class="flex flex-col">
                <div class="bg-indigo-100 text-indigo-800 font-bold text-center py-2 rounded-t-md border-b-2 border-indigo-200 uppercase text-xs tracking-wider">
                    {{ day }}
                </div>
                <div class="bg-gray-50 border border-gray-200 border-t-0 rounded-b-md flex-1 p-2 space-y-3 min-h-[400px]">
                    {% for slot in day_slots %}
                    <div class="bg-white border border-gray-200 p-3 rounded shadow-sm hover:shadow transition relative group cursor-pointer">
                        <div class="text-xs font-bold text-gray-500 mb-1">{{ slot.start_time|time:"h:i A" }} - {{ slot.end_time|time:"h:i A" }}</div>
                        <div class="font-semibold text-indigo-700 text-sm leading-tight mb-1">{{ slot.batch.batch_name }}</div>
                        <div class="text-xs text-gray-600"><i class="fa-solid fa-user-tie mr-1"></i>{{ slot.teacher.display_name }}</div>
                        {% if slot.room_number %}
                        <div class="text-xs text-gray-500 mt-1"><i class="fa-solid fa-location-dot mr-1"></i>{{ slot.room_number }}</div>
                        {% endif %}
                    </div>
                    {% empty %}
                    <div class="text-center text-gray-400 text-xs py-4">No classes</div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}"""

content = content.replace(old_loop, new_loop)

with open('templates/website/timetable.html', 'w') as f:
    f.write(content)
