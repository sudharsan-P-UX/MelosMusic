import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_settings_end = """                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Date Format</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                        <option selected>DD/MM/YYYY</option>
                        <option>MM/DD/YYYY</option>
                        <option>YYYY-MM-DD</option>
                    </select>
                </div>
            </div>"""

new_settings_end = """                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Date Format</label>
                    <select class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500 bg-white">
                        <option selected>DD/MM/YYYY</option>
                        <option>MM/DD/YYYY</option>
                        <option>YYYY-MM-DD</option>
                    </select>
                </div>
            </div>
            
            <h3 class="font-medium text-gray-800 mt-8 mb-6 pb-2 border-b border-gray-100"><i class="fa-solid fa-shield-halved text-indigo-500 mr-2"></i> Security Configuration</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">User password expire date in days</label>
                    <div class="relative">
                        <input type="number" value="90" min="0" max="365" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                        <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                            <span class="text-gray-500 sm:text-sm">days</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">Force users to reset their password after this period. Set to 0 to disable.</p>
                </div>
            </div>"""

content = content.replace(old_settings_end, new_settings_end)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
