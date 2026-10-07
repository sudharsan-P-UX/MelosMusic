with open('templates/website/students.html', 'r') as f:
    content = f.read()

import re

# Replace the modal HTML
old_modal_regex = r'<div id="studentModal" class="fixed inset-0 bg-black bg-opacity-50.*?</div>\s*</div>\s*</div>'

new_modal = """<div id="studentModal" class="fixed inset-0 bg-black bg-opacity-50 hidden flex items-center justify-center z-50 overflow-y-auto">
    <div class="bg-white rounded-lg w-full max-w-4xl mx-4 my-8 relative flex flex-col max-h-[90vh]">
        
        <!-- Modal Header -->
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 rounded-t-lg sticky top-0 z-10">
            <h3 class="text-xl font-bold text-gray-800" id="modalTitle">Add New Student</h3>
            <button type="button" onclick="closeModal()" class="text-gray-400 hover:text-gray-600 transition">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
        </div>
        
        <!-- Modal Body (Scrollable) -->
        <div class="p-6 overflow-y-auto flex-1">
            <form id="studentForm" method="POST" action="{% url 'students' %}">
                {% csrf_token %}
                
                <!-- 1. Personal Information -->
                <div class="mb-6">
                    <h4 class="text-md font-bold text-indigo-700 mb-4 border-b pb-2"><i class="fa-solid fa-user mr-2"></i>Personal Information</h4>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Student Name <span class="text-red-500">*</span></label>
                            <input type="text" id="modalName" name="student_name" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                            <select id="modalGender" name="gender" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                                <option value="">-- Select --</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                            <input type="date" id="modalDob" name="dob" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Email <span class="text-red-500">*</span></label>
                            <input type="email" id="modalEmail" name="email" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Phone <span class="text-red-500">*</span></label>
                            <input type="text" id="modalPhone" name="phone" oninput="this.value = this.value.replace(/[^0-9]/g, '')" maxlength="10" minlength="10" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Parent Name</label>
                            <input type="text" id="modalParentName" name="parent_name" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Parent Phone</label>
                            <input type="text" id="modalParentPhone" name="parent_phone" oninput="this.value = this.value.replace(/[^0-9]/g, '')" maxlength="10" minlength="10" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                            <input type="text" id="modalAddress" name="address" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                    </div>
                </div>

                <!-- 2. Enrollment Information -->
                <div class="mb-6">
                    <h4 class="text-md font-bold text-indigo-700 mb-4 border-b pb-2"><i class="fa-solid fa-graduation-cap mr-2"></i>Enrollment Information</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Course <span class="text-red-500">*</span></label>
                            <select id="modalCourse" name="course_id" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required onchange="updateBatches()">
                                <option value="">-- Select Course --</option>
                                {% for course in courses %}
                                <option value="{{ course.course_id }}" data-days="{{ course.days|default:'' }}">{{ course.course_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Batch Name <span class="text-red-500">*</span></label>
                            <select id="modalBatch" name="batch_id" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required onchange="updateTimeAndDays()">
                                <option value="">-- Select Batch --</option>
                                {% for batch in batches %}
                                <option value="{{ batch.batch_id }}" data-course="{{ batch.course_id }}" data-time="{% if batch.start_time and batch.end_time %}{{ batch.start_time|time:'g:i A' }} - {{ batch.end_time|time:'g:i A' }}{% else %}N/A{% endif %}">{{ batch.batch_name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Class Time (Auto Fill)</label>
                            <input type="text" id="modalClassTime" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-600 outline-none" readonly>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Days (Auto Fill)</label>
                            <input type="text" id="modalDays" name="days" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-600 outline-none" readonly>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Joining Date <span class="text-red-500">*</span></label>
                            <input type="date" id="modalJoiningDate" name="joining_date" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" required>
                        </div>
                    </div>
                </div>

                <!-- 3. Login Information -->
                <div>
                    <h4 class="text-md font-bold text-indigo-700 mb-4 border-b pb-2"><i class="fa-solid fa-lock mr-2"></i>Login Information</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Username (Email used as default)</label>
                            <input type="text" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-50 text-gray-500 outline-none" readonly value="Auto-generated from email">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                            <select id="modalStatus" name="status" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500">
                                <option value="1">Active</option>
                                <option value="0">Inactive</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                            <input type="password" id="modalPassword" name="password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" autocomplete="new-password">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                            <input type="password" id="modalConfirmPassword" name="confirm_password" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500" autocomplete="new-password">
                        </div>
                    </div>
                </div>
            </form>
        </div>
        
        <!-- Modal Footer -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-lg flex justify-end sticky bottom-0 z-10">
            <button type="button" onclick="closeModal()" class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-50 transition mr-2">Cancel</button>
            <button type="button" onclick="document.getElementById('studentForm').submit()" class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition shadow">Save Student</button>
        </div>
        
    </div>
</div>"""

content = re.sub(old_modal_regex, new_modal, content, flags=re.DOTALL)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
