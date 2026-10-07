with open('templates/website/students.html', 'r') as f:
    content = f.read()
    
# Extract everything before {% block content %} and after {% endblock %} if we just want to replace the whole file
new_html = """{% extends "base.html" %}

{% block header %}Student Profile{% endblock %}

{% block content %}
<div class="bg-white rounded border border-gray-200 min-h-screen font-sans text-sm">
    <!-- Header Section -->
    <div class="px-5 py-4 border-b border-gray-200">
        <div class="flex justify-between items-center mb-4">
            <div class="flex items-center space-x-3">
                <h2 class="text-xl font-medium text-gray-800">Manage Students</h2>
                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">Updated just now</span>
                <button class="text-blue-500 hover:text-blue-700 text-xs flex items-center">
                    <i class="fa-solid fa-rotate-right mr-1"></i> Refresh
                </button>
            </div>
        </div>
        
        <!-- Toolbar -->
        <div class="flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <div class="relative">
                    <select class="appearance-none border border-gray-300 rounded px-3 py-1.5 pr-8 text-gray-700 hover:border-gray-400 focus:outline-none bg-white">
                        <option>All ({{ students|length }})</option>
                        <option>Active</option>
                        <option>Inactive</option>
                    </select>
                    <i class="fa-solid fa-chevron-down absolute right-2.5 top-2.5 text-xs text-gray-500"></i>
                </div>
                <div class="relative">
                    <input type="text" placeholder="Search Student" class="border border-gray-300 rounded px-3 py-1.5 w-64 focus:outline-none focus:border-blue-500">
                    <i class="fa-solid fa-magnifying-glass absolute right-3 top-2.5 text-gray-400"></i>
                </div>
                <button class="border border-blue-500 text-blue-600 px-3 py-1.5 rounded hover:bg-blue-50">
                    Filters
                </button>
            </div>
            <div class="flex items-center space-x-2">
                <button onclick="openModal()" class="bg-[#0066cc] hover:bg-blue-700 text-white font-medium py-1.5 px-4 rounded shadow-sm">
                    Quick Add Student
                </button>
                <div class="relative">
                    <button class="border border-gray-300 text-gray-700 px-3 py-1.5 rounded hover:bg-gray-50 flex items-center">
                        More Actions <i class="fa-solid fa-chevron-down ml-2 text-xs"></i>
                    </button>
                </div>
                <button class="border border-gray-300 text-gray-700 p-1.5 rounded hover:bg-gray-50">
                    <i class="fa-solid fa-gear"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- Advanced Filters Row -->
    <div class="px-5 py-3 border-b border-gray-200 bg-gray-50 flex flex-wrap gap-4 items-end">
        <div class="w-40">
            <label class="block text-xs text-gray-500 mb-1">Gender</label>
            <select class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none">
                <option>Type to Search</option>
                <option>Male</option>
                <option>Female</option>
            </select>
        </div>
        <div class="w-40">
            <label class="block text-xs text-gray-500 mb-1">Status</label>
            <select class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none">
                <option>Type to Search</option>
                <option>Active</option>
                <option>Inactive</option>
            </select>
        </div>
        <div class="w-40">
            <label class="block text-xs text-gray-500 mb-1">Modified On</label>
            <select class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none">
                <option>All Time</option>
                <option>Today</option>
                <option>Yesterday</option>
            </select>
        </div>
        <div class="w-40">
            <label class="block text-xs text-gray-500 mb-1">Created On</label>
            <select class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none">
                <option>All Time</option>
                <option>This Week</option>
                <option>This Month</option>
            </select>
        </div>
        <div class="ml-auto">
            <button class="text-blue-600 border border-blue-600 px-3 py-1.5 rounded text-sm hover:bg-blue-50 bg-white">
                Advanced Filters
            </button>
        </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr class="bg-gray-50 text-gray-500 border-b border-gray-200 text-xs uppercase tracking-wider">
                    <th class="py-2.5 px-4 font-semibold w-10 text-center"><input type="checkbox" class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50"></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100 flex items-center">Student Name <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold text-center border-l border-r border-gray-100">Actions</th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Phone <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Email <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Status <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                    <th class="py-2.5 px-4 font-semibold cursor-pointer hover:bg-gray-100">Created On <i class="fa-solid fa-sort ml-1 text-gray-400"></i></th>
                </tr>
            </thead>
            <tbody class="text-gray-700 text-sm">
                {% for student in students %}
                <tr class="border-b border-gray-100 hover:bg-gray-50 transition group">
                    <td class="py-2.5 px-4 text-center"><input type="checkbox" class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-offset-0 focus:ring-blue-200 focus:ring-opacity-50"></td>
                    <td class="py-2.5 px-4 flex items-center space-x-2">
                        <i class="fa-regular fa-star text-gray-300 hover:text-yellow-400 cursor-pointer transition"></i>
                        <span class="text-blue-600 cursor-pointer hover:underline">{{ student.display_name }}</span>
                    </td>
                    <td class="py-2.5 px-4 text-center border-l border-r border-gray-100 text-gray-400 text-lg space-x-3">
                        <i class="fa-solid fa-clipboard-check hover:text-gray-600 cursor-pointer" onclick="openEditModal('{{ student.user_id }}', '{{ student.display_name|escapejs }}', '{{ student.email|escapejs }}', '{{ student.phone|escapejs }}', '{{ student.is_active|yesno:"1,0" }}', '{{ student.gender|escapejs }}', '{{ student.dob|date:"Y-m-d" }}', '{{ student.address|escapejs }}', '{{ student.parent_name|escapejs }}', '{{ student.parent_phone|escapejs }}')" title="Edit"></i>
                        <i class="fa-regular fa-envelope hover:text-gray-600 cursor-pointer" title="Email"></i>
                        <i class="fa-solid fa-phone-flip hover:text-gray-600 cursor-pointer" title="Call"></i>
                        <i class="fa-solid fa-ellipsis hover:text-gray-600 cursor-pointer" title="More"></i>
                        <a href="{% url 'delete_student' student.user_id %}" onclick="return confirm('Are you sure you want to delete {{ student.display_name }}?')" class="text-red-300 hover:text-red-500 transition" title="Delete">
                            <i class="fa-solid fa-trash-can text-sm"></i>
                        </a>
                    </td>
                    <td class="py-2.5 px-4 text-gray-600">{{ student.phone }}</td>
                    <td class="py-2.5 px-4 text-gray-600">{{ student.email }}</td>
                    <td class="py-2.5 px-4">
                        {% if student.is_active %}
                        <span class="text-gray-600">Active</span>
                        {% else %}
                        <span class="text-gray-600">Inactive</span>
                        {% endif %}
                    </td>
                    <td class="py-2.5 px-4 text-gray-500">{{ student.created_date|date:"m/d/Y h:i A" }}</td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="7" class="py-8 text-center text-gray-500">No students found.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Pagination (Static for look) -->
    <div class="px-5 py-3 flex justify-between items-center border-t border-gray-200 text-xs text-gray-500">
        <span>Showing 1 to {{ students|length }} of {{ students|length }} entries</span>
        <div class="flex space-x-1">
            <button class="px-2 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50">Previous</button>
            <button class="px-2 py-1 border border-blue-500 bg-blue-50 text-blue-600 rounded">1</button>
            <button class="px-2 py-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50">Next</button>
        </div>
    </div>
</div>

<!-- ERP Add Student Modal -->
<div id="studentModal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50 overflow-y-auto">
    <div class="bg-white rounded w-full max-w-4xl mx-4 my-8 relative flex flex-col max-h-[90vh]">
        
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 sticky top-0 z-10">
            <h3 class="text-lg font-medium text-gray-800" id="modalTitle">Quick Add Student</h3>
            <button type="button" onclick="closeModal()" class="text-gray-400 hover:text-gray-600 transition">
                <i class="fa-solid fa-xmark text-lg"></i>
            </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1 text-sm text-gray-700">
            <form id="studentForm" method="POST" action="{% url 'students' %}">
                {% csrf_token %}
                
                <div class="mb-8">
                    <h4 class="font-semibold text-gray-800 mb-4 pb-2 border-b uppercase tracking-wider text-xs">Personal Information</h4>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-y-4 gap-x-6">
                        <div>
                            <label class="block mb-1">Student Name <span class="text-red-500">*</span></label>
                            <input type="text" id="modalName" name="student_name" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500" required>
                        </div>
                        <div>
                            <label class="block mb-1">Gender</label>
                            <select id="modalGender" name="gender" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                                <option value="">-- Select --</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div>
                            <label class="block mb-1">Date of Birth</label>
                            <input type="date" id="modalDob" name="dob" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block mb-1">Email <span class="text-red-500">*</span></label>
                            <input type="email" id="modalEmail" name="email" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500" required>
                        </div>
                        <div>
                            <label class="block mb-1">Phone <span class="text-red-500">*</span></label>
                            <input type="text" id="modalPhone" name="phone" oninput="this.value = this.value.replace(/[^0-9]/g, '')" maxlength="10" minlength="10" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500" required>
                        </div>
                        <div>
                            <label class="block mb-1">Parent Name</label>
                            <input type="text" id="modalParentName" name="parent_name" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block mb-1">Parent Phone</label>
                            <input type="text" id="modalParentPhone" name="parent_phone" oninput="this.value = this.value.replace(/[^0-9]/g, '')" maxlength="10" minlength="10" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                        </div>
                        <div class="md:col-span-2">
                            <label class="block mb-1">Address</label>
                            <input type="text" id="modalAddress" name="address" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="font-semibold text-gray-800 mb-4 pb-2 border-b uppercase tracking-wider text-xs">Login Information</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-6">
                        <div>
                            <label class="block mb-1">Status</label>
                            <select id="modalStatus" name="status" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500">
                                <option value="1">Active</option>
                                <option value="0">Inactive</option>
                            </select>
                        </div>
                        <div></div>
                        <div>
                            <label class="block mb-1">Password</label>
                            <input type="password" id="modalPassword" name="password" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500" autocomplete="new-password">
                        </div>
                        <div>
                            <label class="block mb-1">Confirm Password</label>
                            <input type="password" id="modalConfirmPassword" name="confirm_password" class="w-full border border-gray-300 rounded px-3 py-1.5 outline-none focus:border-blue-500" autocomplete="new-password">
                        </div>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 sticky bottom-0 z-10 flex justify-end">
            <button type="button" onclick="closeModal()" class="bg-white border border-gray-300 text-gray-700 px-4 py-1.5 rounded hover:bg-gray-50 transition mr-2">Cancel</button>
            <button type="button" onclick="document.getElementById('studentForm').submit()" class="bg-[#0066cc] text-white px-4 py-1.5 rounded hover:bg-blue-700 transition">Save Student</button>
        </div>
    </div>
</div>

<script>
    const modal = document.getElementById('studentModal');
    const form = document.getElementById('studentForm');
    
    function openModal() {
        form.reset();
        form.action = "{% url 'students' %}";
        document.getElementById('modalTitle').textContent = 'Quick Add Student';
        
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    function openEditModal(id, name, email, phone, status, gender, dob, address, pName, pPhone) {
        form.reset();
        form.action = `/students/update/${id}/`;
        document.getElementById('modalTitle').textContent = 'Edit Student';
        
        document.getElementById('modalName').value = name;
        document.getElementById('modalEmail').value = email;
        document.getElementById('modalPhone').value = phone;
        document.getElementById('modalStatus').value = status;
        
        document.getElementById('modalGender').value = gender;
        document.getElementById('modalDob').value = dob;
        document.getElementById('modalAddress').value = address;
        document.getElementById('modalParentName').value = pName;
        document.getElementById('modalParentPhone').value = pPhone;
        
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    
    function closeModal() {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
</script>
{% endblock %}
"""

with open('templates/website/students.html', 'w') as f:
    f.write(new_html)
