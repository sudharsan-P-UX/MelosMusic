with open('templates/website/students.html', 'r') as f:
    content = f.read()

import re

# We want to replace the Class, Class Time, and Days section
old_section_regex = r'<div class="grid grid-cols-2 gap-4">\s*<div>\s*<label class="block text-sm font-medium text-gray-700 mb-1">Class</label>.*?<label class="inline-flex items-center"><input type="checkbox" name="days" value="Sun" class="form-checkbox text-indigo-600 rounded"><span class="ml-1 mr-3">Sun</span></label>\s*</div>\s*</div>'

new_section = """<div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Class</label>
                        <select id="modalCourse" name="course_id" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" onchange="updateBatches()">
                            <option value="">-- Select Class --</option>
                            {% for course in courses %}
                            <option value="{{ course.course_id }}" data-days="{{ course.days|default:'' }}">{{ course.course_name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Batch Name</label>
                        <select id="modalBatch" name="batch_id" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" onchange="updateTimeAndDays()">
                            <option value="">-- Select Batch --</option>
                            {% for batch in batches %}
                            <option value="{{ batch.batch_id }}" data-course="{{ batch.course_id }}" data-time="{% if batch.start_time and batch.end_time %}{{ batch.start_time|time:'g:i A' }} - {{ batch.end_time|time:'g:i A' }}{% else %}N/A{% endif %}">{{ batch.batch_name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Class Time</label>
                        <input type="text" id="modalClassTime" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-600 outline-none" readonly placeholder="Auto-filled from Batch">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Days</label>
                        <input type="text" id="modalDays" name="days" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-600 outline-none" readonly placeholder="Auto-filled from Class">
                    </div>
                </div>

                <script>
                    function updateBatches() {
                        const courseId = document.getElementById('modalCourse').value;
                        const batchSelect = document.getElementById('modalBatch');
                        const options = batchSelect.options;
                        
                        let firstValid = null;
                        
                        for (let i = 1; i < options.length; i++) {
                            const option = options[i];
                            if (!courseId || option.getAttribute('data-course') === courseId) {
                                option.style.display = '';
                                if (!firstValid) firstValid = option.value;
                            } else {
                                option.style.display = 'none';
                            }
                        }
                        
                        batchSelect.value = '';
                        updateTimeAndDays();
                    }
                    
                    function updateTimeAndDays() {
                        const batchSelect = document.getElementById('modalBatch');
                        const courseSelect = document.getElementById('modalCourse');
                        
                        const timeInput = document.getElementById('modalClassTime');
                        const daysInput = document.getElementById('modalDays');
                        
                        if (batchSelect.selectedIndex > 0) {
                            timeInput.value = batchSelect.options[batchSelect.selectedIndex].getAttribute('data-time');
                        } else {
                            timeInput.value = '';
                        }
                        
                        if (courseSelect.selectedIndex > 0) {
                            daysInput.value = courseSelect.options[courseSelect.selectedIndex].getAttribute('data-days');
                        } else {
                            daysInput.value = '';
                        }
                    }
                </script>"""

content = re.sub(old_section_regex, new_section, content, flags=re.DOTALL)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
