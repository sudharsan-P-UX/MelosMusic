import re

with open('templates/website/admin_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r"""(<div>\n\s+<label class="block text-sm font-medium text-gray-700 mb-1">User password expire date in days</label>\n\s+<div class="relative">.*?</div>\n\s+<p class="text-xs text-gray-500 mt-1">Force users to reset their password after this period\. Set to 0 to disable\.</p>\n\s+</div>)"""

new_fields = r"""\1
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number Length (Country Format)</label>
                    <div class="relative">
                        <input type="number" value="10" min="5" max="20" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                        <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                            <span class="text-gray-500 sm:text-sm">digits</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">Maximum allowed length for user phone numbers.</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email Maximum Length</label>
                    <div class="relative">
                        <input type="number" value="255" min="10" max="255" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                        <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                            <span class="text-gray-500 sm:text-sm">chars</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">Maximum allowed length for user email addresses.</p>
                </div>"""

html = re.sub(pattern, new_fields, html, flags=re.DOTALL)

with open('templates/website/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
