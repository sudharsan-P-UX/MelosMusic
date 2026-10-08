import re

with open('templates/website/teachers.html', 'r') as f:
    content = f.read()

old_header = """    <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 class="text-lg font-medium text-gray-800">Teachers Directory</h2>
        <!-- Add Button Right Side -->
        <button onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded shadow flex items-center transition">
            <i class="fa-solid fa-plus mr-2"></i> Add Teacher
        </button>
    </div>"""

new_header = """    <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-medium text-gray-800">Teachers Directory</h2>
        </div>
        
        <form method="GET" action="{% url 'teachers' %}" class="flex flex-wrap gap-3 items-end pb-2">
            
            <div class="relative">
                <select name="status_filter" class="appearance-none border border-gray-300 rounded px-3 py-1.5 pr-8 text-sm text-gray-700 hover:border-gray-400 focus:outline-none bg-white h-[34px]">
                    <option value="">All ({{ teachers|length }})</option>
                    <option value="1" {% if request.GET.status_filter == '1' %}selected{% endif %}>Active</option>
                    <option value="0" {% if request.GET.status_filter == '0' %}selected{% endif %}>Inactive</option>
                </select>
                <i class="fa-solid fa-chevron-down absolute right-2.5 top-2.5 text-xs text-gray-500"></i>
            </div>
            
            <div class="relative">
                <input type="text" name="search" value="{{ request.GET.search|default:'' }}" placeholder="Search Teacher" class="border border-gray-300 rounded px-3 py-1.5 w-48 text-sm focus:outline-none focus:border-blue-500 h-[34px]">
                <i class="fa-solid fa-magnifying-glass absolute right-3 top-2.5 text-gray-400"></i>
            </div>
            
            <div class="w-36">
                <label class="block text-xs text-gray-500 mb-1">From Date</label>
                <input type="date" name="from_date" value="{{ request.GET.from_date|default:'' }}" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none h-[34px]">
            </div>
            
            <div class="w-36">
                <label class="block text-xs text-gray-500 mb-1">To Date</label>
                <input type="date" name="to_date" value="{{ request.GET.to_date|default:'' }}" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-600 outline-none h-[34px]">
            </div>
            
            <div class="flex space-x-2">
                <button type="submit" class="bg-gray-100 border border-gray-300 text-gray-700 px-4 py-1.5 rounded text-sm hover:bg-gray-200 h-[34px] flex items-center shadow-sm">
                    <i class="fa-solid fa-filter mr-1.5"></i> Apply
                </button>
                <a href="{% url 'teachers' %}" class="bg-white border border-gray-300 text-gray-600 px-4 py-1.5 rounded text-sm hover:bg-gray-50 h-[34px] flex items-center shadow-sm">
                    Clear
                </a>
            </div>
            
            <div class="ml-auto">
                <button type="button" onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-1.5 px-4 rounded shadow-sm text-sm h-[34px] flex items-center">
                    <i class="fa-solid fa-plus mr-1.5"></i> Add Teacher
                </button>
            </div>
        </form>
    </div>"""

content = content.replace(old_header, new_header)

with open('templates/website/teachers.html', 'w') as f:
    f.write(content)
