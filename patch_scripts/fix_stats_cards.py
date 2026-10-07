import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_stats_block = """        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white p-4 rounded border border-gray-200 shadow-sm flex items-center">
                <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center text-xl mr-4"><i class="fa-solid fa-shield-halved"></i></div>
                <div>
                    <div class="text-xs text-gray-500 font-medium uppercase tracking-wider mb-1">Total Roles</div>
                    <div class="text-2xl font-bold text-gray-800">{{ roles|length }}</div>
                </div>
            </div>
            <div class="bg-white p-4 rounded border border-gray-200 shadow-sm flex items-center">
                <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-xl mr-4"><i class="fa-solid fa-users"></i></div>
                <div>
                    <div class="text-xs text-gray-500 font-medium uppercase tracking-wider mb-1">Assigned Users</div>
                    <div class="text-2xl font-bold text-gray-800">{{ users|length }}</div>
                </div>
            </div>
        </div>"""

new_stats_block = """        <!-- Stats -->
        <div class="flex flex-wrap gap-6">
            <div class="bg-white p-4 rounded border border-gray-200 shadow-sm flex items-center justify-between w-72">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center text-xl mr-4"><i class="fa-solid fa-shield-halved"></i></div>
                    <div class="text-xs text-gray-500 font-medium uppercase tracking-wider">Total Roles</div>
                </div>
                <div class="text-3xl font-bold text-gray-800">{{ roles|length }}</div>
            </div>
            <div class="bg-white p-4 rounded border border-gray-200 shadow-sm flex items-center justify-between w-72">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-xl mr-4"><i class="fa-solid fa-users"></i></div>
                    <div class="text-xs text-gray-500 font-medium uppercase tracking-wider">Assigned Users</div>
                </div>
                <div class="text-3xl font-bold text-gray-800">{{ users|length }}</div>
            </div>
        </div>"""

content = content.replace(old_stats_block, new_stats_block)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
