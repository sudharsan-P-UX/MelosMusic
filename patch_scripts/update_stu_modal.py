with open('templates/website/student_attendance.html', 'r') as f:
    content = f.read()

modal_html = """
<!-- Add Attendance Modal -->
<div id="addAttendanceModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 hidden items-center justify-center z-50 transition-opacity">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 flex-shrink-0">
            <h3 class="text-lg font-bold text-gray-800">Mark Student Attendance</h3>
            <button type="button" onclick="closeModal()" class="text-gray-400 hover:text-gray-600">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>
        
        <form method="POST" action="{% url 'student_attendance' %}" class="flex flex-col flex-1 overflow-hidden" autocomplete="off">
            {% csrf_token %}
            <div class="p-6 overflow-y-auto space-y-4 flex-1">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
                    <input type="date" name="attendance_date" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Batch</label>
                    <select name="batch_id" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="">-- Select Batch --</option>
                        {% for batch in batches %}
                        <option value="{{ batch.batch_id }}">{{ batch.batch_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Student</label>
                    <select name="student_id" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="">-- Select Student --</option>
                        {% for student in students %}
                        <option value="{{ student.user_id }}">{{ student.display_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                    <select name="status" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="1">Present</option>
                        <option value="2">Absent</option>
                        <option value="3">Late</option>
                        <option value="4">Leave</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Remarks</label>
                    <input type="text" name="remarks" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" placeholder="e.g. Late due to traffic">
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end space-x-3 flex-shrink-0">
                <button type="button" onclick="closeModal()" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition">Cancel</button>
                <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 shadow transition">Save</button>
            </div>
        </form>
    </div>
</div>

<script>
    const modal = document.getElementById('addAttendanceModal');
    
    function openModal() {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Auto-fill today's date
        document.querySelector('input[name="attendance_date"]').valueAsDate = new Date();
    }
    
    function closeModal() {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
</script>
"""

content = content.replace('<button class="bg-indigo-600 hover:bg-indigo-700', '<button onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700')
content = content.replace('{% endblock %}', modal_html + '\n{% endblock %}')

with open('templates/website/student_attendance.html', 'w') as f:
    f.write(content)
