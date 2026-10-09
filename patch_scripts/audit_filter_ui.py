import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_audit_header = """    <!-- Audit Logs Tab -->
    <div x-show="tab === 'audit'" x-transition class="space-y-4" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                <h3 class="font-medium text-gray-800">Recent Activity Logs</h3>
            </div>"""

new_audit_header = """    <!-- Audit Logs Tab -->
    <div x-show="tab === 'audit'" x-transition class="space-y-4" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex flex-wrap gap-4 justify-between items-center bg-gray-50">
                <h3 class="font-medium text-gray-800">Recent Activity Logs</h3>
                <form method="GET" action="" class="flex">
                    <input type="hidden" name="tab" value="audit">
                    <input type="text" name="audit_search" value="{{ request.GET.audit_search }}" placeholder="Search user or remarks..." class="border border-gray-300 rounded-l px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:border-indigo-500 w-64 bg-white">
                    <button type="submit" class="bg-gray-100 hover:bg-gray-200 border border-l-0 border-gray-300 rounded-r px-3 py-1.5 text-gray-600 transition-colors">
                        <i class="fa-solid fa-search"></i>
                    </button>
                    {% if request.GET.audit_search %}
                    <a href="?tab=audit" class="ml-2 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded px-3 py-1.5 text-gray-600 transition-colors flex items-center justify-center" title="Clear Filter">
                        <i class="fa-solid fa-times text-xs"></i>
                    </a>
                    {% endif %}
                </form>
            </div>"""

content = content.replace(old_audit_header, new_audit_header)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
