import re

with open('templates/website/student_attendance.html', 'r') as f:
    content = f.read()

# Add a button
old_buttons = """<button onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center">
            <i class="fa-solid fa-plus mr-2"></i> Add Attendance
        </button>"""
        
new_buttons = """<div class="flex space-x-3">
            <button onclick="openLeaveModal()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center">
                <i class="fa-solid fa-calendar-minus mr-2"></i> Apply Leave
            </button>
            <button onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center">
                <i class="fa-solid fa-plus mr-2"></i> Add Attendance
            </button>
        </div>"""
        
content = content.replace(old_buttons, new_buttons)

# Add Leave Modal
leave_modal = """
<!-- Apply Leave Modal -->
<div id="applyLeaveModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 hidden items-center justify-center z-50 transition-opacity">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 flex-shrink-0">
            <h3 class="text-lg font-bold text-gray-800">Apply for Leave</h3>
            <button type="button" onclick="closeLeaveModal()" class="text-gray-400 hover:text-gray-600">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>
        <form method="POST" action="" class="flex flex-col flex-1 overflow-hidden">
            {% csrf_token %}
            <input type="hidden" name="action" value="apply_leave">
            <div class="p-6 overflow-y-auto space-y-4 flex-1">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Student</label>
                    <select name="student_id" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-purple-500">
                        <option value="">-- Select Student --</option>
                        {% for s in students %}
                        <option value="{{ s.user.user_id }}" {% if user.user_id == s.user.user_id %}selected{% endif %}>{{ s.user.display_name|default:s.user.first_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Leave Type</label>
                    <select name="request_type" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-purple-500">
                        <option value="Sick Leave">Sick Leave</option>
                        <option value="Casual Leave">Casual Leave</option>
                        <option value="Emergency Leave">Emergency Leave</option>
                        <option value="Vacation">Vacation</option>
                    </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">From Date</label>
                        <input type="date" name="from_date" id="leave_from" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-purple-500" onchange="calcDays()">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">To Date</label>
                        <input type="date" name="to_date" id="leave_to" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-purple-500" onchange="calcDays()">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">No. of Days</label>
                    <input type="number" name="no_of_days" id="leave_days" readonly class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-500">
                </div>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end space-x-3 flex-shrink-0">
                <button type="button" onclick="closeLeaveModal()" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 font-medium transition">Cancel</button>
                <button type="submit" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md font-medium transition shadow-sm">Submit Request</button>
            </div>
        </form>
    </div>
</div>

<script>
    function openLeaveModal() {
        document.getElementById('applyLeaveModal').classList.remove('hidden');
        document.getElementById('applyLeaveModal').classList.add('flex');
    }
    function closeLeaveModal() {
        document.getElementById('applyLeaveModal').classList.add('hidden');
        document.getElementById('applyLeaveModal').classList.remove('flex');
    }
    function calcDays() {
        const fromDate = document.getElementById('leave_from').value;
        const toDate = document.getElementById('leave_to').value;
        if(fromDate && toDate) {
            const start = new Date(fromDate);
            const end = new Date(toDate);
            if(end >= start) {
                const diffTime = Math.abs(end - start);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                document.getElementById('leave_days').value = diffDays;
            } else {
                document.getElementById('leave_days').value = 0;
            }
        }
    }
</script>
"""

content = content.replace("<!-- Add Attendance Modal -->", leave_modal + "\n<!-- Add Attendance Modal -->")

with open('templates/website/student_attendance.html', 'w') as f:
    f.write(content)
