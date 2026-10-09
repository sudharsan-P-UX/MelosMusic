template_content = """{% extends 'base.html' %}
{% block content %}
<div class="mb-6">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold text-gray-800">{{ page_title }}</h2>
        <div class="flex space-x-3">
            {% if menu_access.add %}
            <button onclick="openLeaveModal()" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center">
                <i class="fa-solid fa-paper-plane mr-2"></i> Attendance Request
            </button>
            {% endif %}
        </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <form method="GET" action="" class="flex flex-wrap gap-4 items-end">
            {% if 'Student' in page_title %}
            <div class="w-48">
                <select name="batch_id" class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                    <option value="">Select Batch</option>
                    {% for b in batches %}
                        <option value="{{ b.batch_id }}" {% if selected_batch == b.batch_id|stringformat:"s" %}selected{% endif %}>{{ b.batch_name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="w-48">
                <select name="student_id" class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                    <option value="">Select Student</option>
                    {% for s in students %}
                        <option value="{{ s.user_id }}" {% if selected_student == s.user_id|stringformat:"s" %}selected{% endif %}>{{ s.display_name }}</option>
                    {% endfor %}
                </select>
            </div>
            {% else %}
            <div class="w-48">
                <select name="teacher_id" class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
                    <option value="">Select Teacher</option>
                    {% for t in teachers %}
                        <option value="{{ t.user_id }}" {% if selected_teacher == t.user_id|stringformat:"s" %}selected{% endif %}>{{ t.display_name }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endif %}
            <div class="w-40">
                <input type="date" name="date" value="{{ selected_date }}" class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
            </div>
            <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center h-[38px]">
                <i class="fa-solid fa-filter mr-2"></i> Filter
            </button>
            <a href="?tab={% if 'Student' in page_title %}students{% else %}teachers{% endif %}" class="bg-white border border-red-500 text-red-500 hover:bg-red-50 px-4 py-2 rounded-md font-medium shadow-sm transition flex items-center h-[38px]">
                <i class="fa-solid fa-arrow-rotate-right mr-2"></i> Reset
            </a>
        </form>
    </div>

    <!-- Attendance Grid -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden flex flex-col">
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
            <h3 class="font-bold text-gray-800">Attendance Details</h3>
        </div>
        <div class="overflow-x-auto flex-1">
            <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 border-b border-gray-200 text-gray-700 text-xs uppercase tracking-wider text-left">
                    <tr>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap w-16">#</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap">Date (From - To)</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap">Name</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">No Of Days</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Request Type</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Status</th>
                        <th class="py-3 px-4 font-semibold whitespace-nowrap text-center">Manager Approval On</th>
                    </tr>
                </thead>
                <tbody class="text-sm">
                    {% for d in details %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                        <td class="py-3 px-4 text-gray-600">{{ forloop.counter }}</td>
                        <td class="py-3 px-4">{{ d.from_date|date:"d-b-Y" }} to {{ d.to_date|date:"d-b-Y" }}</td>
                        <td class="py-3 px-4 font-medium text-gray-800">{{ d.user.display_name }}</td>
                        <td class="py-3 px-4 text-center">{{ d.no_of_days }}</td>
                        <td class="py-3 px-4 text-center">
                            <span class="px-2.5 py-1 bg-gray-100 text-gray-700 rounded-md text-xs font-medium">{{ d.request_type }}</span>
                        </td>
                        <td class="py-3 px-4 text-center">
                            {% if d.manager_approval_status == 'Approved' %}
                                <span class="px-2.5 py-1 bg-emerald-100 text-emerald-700 rounded-md text-xs font-medium">Approved</span>
                            {% elif d.manager_approval_status == 'Rejected' %}
                                <span class="px-2.5 py-1 bg-red-100 text-red-700 rounded-md text-xs font-medium">Rejected</span>
                            {% else %}
                                <span class="px-2.5 py-1 bg-yellow-100 text-yellow-700 rounded-md text-xs font-medium">Pending</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center text-gray-500 text-sm">
                            {{ d.manager_approval_on|date:"d-b-Y h:i A"|default:"-" }}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="7" class="py-8 text-center text-gray-500">
                            No attendance records found. Click "Attendance Request" to submit a new request.
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Apply Leave Modal -->
<div id="leaveModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 hidden items-center justify-center z-50 transition-opacity">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 overflow-hidden flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 flex-shrink-0">
            <h3 class="text-lg font-bold text-gray-800">Submit Attendance Request</h3>
            <button type="button" onclick="closeLeaveModal()" class="text-gray-400 hover:text-gray-600">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>
        <form method="POST" action="" class="flex flex-col flex-1 overflow-hidden" onsubmit="return validateLeaveForm()">
            {% csrf_token %}
            <input type="hidden" name="action" value="apply_leave">
            {% if 'Student' in page_title %}
            <input type="hidden" name="student_id" value="{{ user.user_id }}">
            {% else %}
            <input type="hidden" name="teacher_id" value="{{ user.user_id }}">
            {% endif %}
            
            <div class="p-6 overflow-y-auto flex-1 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Request Type <span class="text-red-500">*</span></label>
                    <select name="request_type" required class="w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm">
                        <option value="">Select Type</option>
                        <option value="Leave">Leave</option>
                        <option value="Permission">Permission</option>
                        <option value="On Duty">On Duty</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">From Date <span class="text-red-500">*</span></label>
                    <input type="date" name="from_date" id="leave_from_date" required class="w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm" onchange="calculateLeaveDays()">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">To Date <span class="text-red-500">*</span></label>
                    <input type="date" name="to_date" id="leave_to_date" required class="w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 text-sm" onchange="calculateLeaveDays()">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">No. of Days</label>
                    <input type="number" name="no_of_days" id="leave_no_of_days" readonly class="w-full bg-gray-50 border-gray-300 rounded-md shadow-sm text-sm text-gray-500">
                </div>
            </div>
            
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end space-x-3 flex-shrink-0">
                <button type="button" onclick="closeLeaveModal()" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 font-medium text-sm transition shadow-sm">
                    Cancel
                </button>
                <button type="submit" class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 font-medium text-sm transition shadow-sm">
                    Submit Request
                </button>
            </div>
        </form>
    </div>
</div>

<script>
    function openLeaveModal() {
        document.getElementById('leaveModal').classList.remove('hidden');
        document.getElementById('leaveModal').classList.add('flex');
    }
    
    function closeLeaveModal() {
        document.getElementById('leaveModal').classList.add('hidden');
        document.getElementById('leaveModal').classList.remove('flex');
    }

    function calculateLeaveDays() {
        const fromDateStr = document.getElementById('leave_from_date').value;
        const toDateStr = document.getElementById('leave_to_date').value;
        const noOfDaysInput = document.getElementById('leave_no_of_days');
        
        if (fromDateStr && toDateStr) {
            const start = new Date(fromDateStr);
            const end = new Date(toDateStr);
            const diffTime = end - start;
            if (diffTime >= 0) {
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                noOfDaysInput.value = diffDays;
            } else {
                noOfDaysInput.value = '';
            }
        }
    }

    function validateLeaveForm() {
        const fromDateStr = document.getElementById('leave_from_date').value;
        const toDateStr = document.getElementById('leave_to_date').value;
        if (fromDateStr && toDateStr) {
            if (new Date(toDateStr) < new Date(fromDateStr)) {
                alert('To Date cannot be earlier than From Date.');
                return false;
            }
        }
        return true;
    }
</script>
{% endblock %}
"""

with open('templates/website/student_attendance_v2.html', 'w', encoding='utf-8') as f:
    f.write(template_content)

with open('templates/website/teacher_attendance_v2.html', 'w', encoding='utf-8') as f:
    f.write(template_content)
