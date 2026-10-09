import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_form = """                <form method="GET" action="" class="flex">
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
                </form>"""

new_form = """                <form method="GET" action="" class="flex flex-wrap gap-2 items-center">
                    <input type="hidden" name="tab" value="audit">
                    
                    <select name="audit_user" class="border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:border-indigo-500 bg-white">
                        <option value="">All Users</option>
                        {% for u in users %}
                        <option value="{{ u.user_id }}" {% if request.GET.audit_user == u.user_id|stringformat:"s" %}selected{% endif %}>{{ u.display_name|default:u.first_name }}</option>
                        {% endfor %}
                    </select>
                    
                    <input type="date" name="audit_from" value="{{ request.GET.audit_from }}" class="border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:border-indigo-500 bg-white" title="From Date">
                    
                    <span class="text-gray-400 text-xs">to</span>
                    
                    <input type="date" name="audit_to" value="{{ request.GET.audit_to }}" class="border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:border-indigo-500 bg-white" title="To Date">
                    
                    <select name="audit_status" class="border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:border-indigo-500 bg-white">
                        <option value="">All Statuses</option>
                        <option value="Success" {% if request.GET.audit_status == 'Success' %}selected{% endif %}>Success</option>
                        <option value="Failed" {% if request.GET.audit_status == 'Failed' %}selected{% endif %}>Failed</option>
                    </select>
                    
                    <button type="submit" class="bg-[#4f46e5] hover:bg-indigo-700 border border-[#4f46e5] text-white rounded px-3 py-1.5 text-xs transition-colors flex items-center">
                        <i class="fa-solid fa-filter mr-1"></i> Filter
                    </button>
                    
                    {% if request.GET.audit_user or request.GET.audit_status or request.GET.audit_from or request.GET.audit_to %}
                    <a href="?tab=audit" class="bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded px-3 py-1.5 text-gray-600 transition-colors flex items-center justify-center" title="Clear Filter">
                        <i class="fa-solid fa-times text-xs"></i>
                    </a>
                    {% endif %}
                </form>"""

content = content.replace(old_form, new_form)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
