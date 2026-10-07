import re

# 1. Update website/views.py to handle create_user
with open('website/views.py', 'r') as f:
    views_content = f.read()

view_logic = """    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_user':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = request.POST.get('password', '')
            role_id = request.POST.get('role_id')
            
            try:
                role = Role.objects.get(role_id=role_id)
                User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip(),
                    email=email,
                    phone=phone,
                    password=password,
                    role=role
                )
            except Exception as e:
                print(e)
            return redirect('/admin-dashboard/?tab=users')

    tab = request.GET.get('tab', 'dashboard')"""

if "action == 'create_user'" not in views_content:
    views_content = views_content.replace("tab = request.GET.get('tab', 'dashboard')", view_logic)
    with open('website/views.py', 'w') as f:
        f.write(views_content)


# 2. Update templates/website/admin_dashboard.html
with open('templates/website/admin_dashboard.html', 'r') as f:
    template = f.read()

# Add to x-data
template = template.replace(
    "x-data=\"{ tab: '{{ active_tab|default:'roles' }}', showCreateRoleModal: false }\"", 
    "x-data=\"{ tab: '{{ active_tab|default:'roles' }}', showCreateRoleModal: false, showAddUserModal: false }\""
)

# Bind button click
template = template.replace(
    "<button class=\"bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition\">\n                    <i class=\"fa-solid fa-user-plus mr-1\"></i> Add User\n                  </button>",
    "<button @click=\"showAddUserModal = true\" class=\"bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition\">\n                    <i class=\"fa-solid fa-user-plus mr-1\"></i> Add User\n                  </button>"
)

# The modal markup
modal_markup = """
    <!-- Add User Modal -->
    <div x-show="showAddUserModal" style="display: none;" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <!-- Background overlay -->
            <div x-show="showAddUserModal" x-transition.opacity class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showAddUserModal = false"></div>
            
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            
            <!-- Modal panel -->
            <div x-show="showAddUserModal" x-transition class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <form method="POST" action="">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="create_user">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">Create New User</h3>
                        <div class="space-y-4">
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">First Name (Username)</label>
                                    <input type="text" name="first_name" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                                    <input type="text" name="last_name" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                <input type="email" name="email" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                                <input type="text" name="phone" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                <input type="password" name="password" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
                                <select name="role_id" required class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                                    <option value="">Select a role...</option>
                                    {% for role in roles %}
                                        <option value="{{ role.role_id }}">{{ role.role_name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse border-t border-gray-200">
                        <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm transition">
                            Create User
                        </button>
                        <button type="button" @click="showAddUserModal = false" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
"""

if 'showAddUserModal = false' not in template:
    # Insert modal before closing </div> of the x-data scope
    template = template.replace('</div>\n{% endblock %}', modal_markup + '</div>\n{% endblock %}')
    with open('templates/website/admin_dashboard.html', 'w') as f:
        f.write(template)
