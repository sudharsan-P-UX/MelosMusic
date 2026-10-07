import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_placeholder = """    <!-- Other Tabs Placeholder -->
    <div x-show="tab !== 'roles'" x-transition class="bg-white rounded border border-gray-200 p-12 text-center text-gray-500 shadow-sm flex flex-col items-center justify-center">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <i class="fa-solid fa-person-digging text-2xl text-gray-400"></i>
        </div>
        <h3 class="text-lg font-medium text-gray-700">Under Construction</h3>
        <p class="mt-2 text-sm text-gray-500 max-w-sm">The <span x-text="tab" class="font-semibold uppercase text-indigo-500"></span> module is currently being built and will be available soon.</p>
    </div>"""

new_tabs = """    <!-- Dashboard Tab -->
    <div x-show="tab === 'dashboard'" x-transition class="space-y-6" style="display: none;">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-white p-6 rounded border border-gray-200 shadow-sm flex flex-col">
                <div class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">Total Users</div>
                <div class="text-3xl font-bold text-gray-800">{{ users|length }}</div>
            </div>
            <div class="bg-white p-6 rounded border border-gray-200 shadow-sm flex flex-col">
                <div class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">Active Roles</div>
                <div class="text-3xl font-bold text-gray-800">{{ roles|length }}</div>
            </div>
            <div class="bg-white p-6 rounded border border-gray-200 shadow-sm flex flex-col">
                <div class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">Menus Configured</div>
                <div class="text-3xl font-bold text-gray-800">{{ menus|length }}</div>
            </div>
            <div class="bg-white p-6 rounded border border-gray-200 shadow-sm flex flex-col">
                <div class="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">System Status</div>
                <div class="text-3xl font-bold text-emerald-500 flex items-center"><i class="fa-solid fa-circle-check text-xl mr-2"></i> Online</div>
            </div>
        </div>
    </div>
    
    <!-- User Management Tab -->
    <div x-show="tab === 'users'" x-transition class="space-y-6" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                <h3 class="font-medium text-gray-800">System Users</h3>
                <button class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-user-plus mr-1"></i> Add User
                </button>
            </div>
            <table class="w-full text-left border-collapse text-sm">
                <thead>
                    <tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-3 px-4 font-medium">Name</th>
                        <th class="py-3 px-4 font-medium">Username</th>
                        <th class="py-3 px-4 font-medium">Email</th>
                        <th class="py-3 px-4 font-medium">Role</th>
                        <th class="py-3 px-4 font-medium text-center">Status</th>
                        <th class="py-3 px-4 font-medium text-center">Actions</th>
                    </tr>
                </thead>
                <tbody class="text-gray-700">
                    {% for u in users %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="py-3 px-4 font-medium text-gray-800">{{ u.display_name|default:u.first_name }}</td>
                        <td class="py-3 px-4 text-gray-600">{{ u.first_name }}</td>
                        <td class="py-3 px-4 text-gray-600">{{ u.email|default:"-" }}</td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-medium">{{ u.role.role_name|default:"Unassigned" }}</span>
                        </td>
                        <td class="py-3 px-4 text-center">
                            {% if u.is_active %}
                            <span class="text-emerald-500 font-medium text-xs"><i class="fa-solid fa-circle text-[8px] mr-1 inline-block align-middle"></i>Active</span>
                            {% else %}
                            <span class="text-red-500 font-medium text-xs">Inactive</span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center space-x-2">
                            <button class="text-indigo-400 hover:text-indigo-600 bg-indigo-50 hover:bg-indigo-100 p-1.5 rounded transition"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 p-1.5 rounded transition"><i class="fa-solid fa-trash-can"></i></button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Menu Permissions Tab -->
    <div x-show="tab === 'menu'" x-transition class="space-y-6" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                <h3 class="font-medium text-gray-800">Menu Master List</h3>
                <button class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-plus mr-1"></i> Add Menu
                </button>
            </div>
            <table class="w-full text-left border-collapse text-sm">
                <thead>
                    <tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-3 px-4 font-medium w-16 text-center">ID</th>
                        <th class="py-3 px-4 font-medium">Menu Name</th>
                        <th class="py-3 px-4 font-medium">URL Route</th>
                        <th class="py-3 px-4 font-medium text-center">Status</th>
                        <th class="py-3 px-4 font-medium text-center">Actions</th>
                    </tr>
                </thead>
                <tbody class="text-gray-700">
                    {% for m in menus %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="py-3 px-4 text-center text-gray-500">{{ m.menu_id }}</td>
                        <td class="py-3 px-4 font-medium text-gray-800"><i class="fa-solid fa-folder text-gray-300 mr-2"></i> {{ m.menu_name }}</td>
                        <td class="py-3 px-4 text-gray-500 font-mono text-xs">{{ m.url_page }}</td>
                        <td class="py-3 px-4 text-center">
                            {% if m.is_active %}
                            <span class="text-emerald-500"><i class="fa-solid fa-toggle-on text-lg"></i></span>
                            {% else %}
                            <span class="text-gray-400"><i class="fa-solid fa-toggle-off text-lg"></i></span>
                            {% endif %}
                        </td>
                        <td class="py-3 px-4 text-center space-x-2">
                            <button class="text-indigo-400 hover:text-indigo-600 bg-indigo-50 hover:bg-indigo-100 p-1.5 rounded transition"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-red-400 hover:text-red-600 bg-red-50 hover:bg-red-100 p-1.5 rounded transition"><i class="fa-solid fa-trash-can"></i></button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- System Settings Tab -->
    <div x-show="tab === 'settings'" x-transition class="space-y-6" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm p-6">
            <h3 class="font-medium text-gray-800 mb-6 pb-2 border-b border-gray-100">General Configuration</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Application Name</label>
                    <input type="text" value="Melo's Music" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Support Email</label>
                    <input type="email" value="support@melosmusic.com" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Timezone</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                        <option>UTC (Coordinated Universal Time)</option>
                        <option selected>Asia/Kolkata (IST)</option>
                        <option>America/New_York (EST)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Date Format</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                        <option selected>DD/MM/YYYY</option>
                        <option>MM/DD/YYYY</option>
                        <option>YYYY-MM-DD</option>
                    </select>
                </div>
            </div>
            <div class="mt-8 flex justify-end">
                <button class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 shadow-sm transition">
                    Save Settings
                </button>
            </div>
        </div>
    </div>
    
    <!-- Audit Logs Tab -->
    <div x-show="tab === 'audit'" x-transition class="space-y-6" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                <h3 class="font-medium text-gray-800">Recent Activity Logs</h3>
            </div>
            <table class="w-full text-left border-collapse text-sm">
                <thead>
                    <tr class="border-b border-gray-200 text-gray-500 bg-gray-50">
                        <th class="py-3 px-4 font-medium w-48">Timestamp</th>
                        <th class="py-3 px-4 font-medium">User</th>
                        <th class="py-3 px-4 font-medium">Action / Remarks</th>
                    </tr>
                </thead>
                <tbody class="text-gray-700">
                    {% for log in audit_logs %}
                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="py-3 px-4 text-gray-500 text-xs">{{ log.login_date|date:"Y-m-d H:i:s" }}</td>
                        <td class="py-3 px-4 font-medium text-gray-800">{{ log.user.display_name|default:log.user.first_name }}</td>
                        <td class="py-3 px-4 text-gray-600">
                            {% if "Success" in log.remarks %}
                                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded text-xs mr-2">Login</span>
                            {% else %}
                                <span class="px-2 py-0.5 bg-red-100 text-red-700 rounded text-xs mr-2">Failed</span>
                            {% endif %}
                            {{ log.remarks }}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="3" class="py-8 text-center text-gray-500">No activity logs found.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>"""

content = content.replace(old_placeholder, new_tabs)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
