import re

with open('templates/website/events_dashboard.html', 'r') as f:
    content = f.read()

pattern = r'<div class="flex flex-wrap gap-4 items-end mb-6">.*?<div class="flex-1 min-w-\[200px\]">.*?<input type="text" placeholder="Search event name.*?<div class="flex space-x-2">.*?<i class="fa-solid fa-rotate-right"></i>.*?</div>\s*</div>'

new_filter_block = """<form method="GET" action="{% url 'events_dashboard' %}" class="flex flex-wrap gap-4 items-end mb-6">
                <input type="hidden" name="tab" value="list">
                <div class="flex-1 min-w-[200px]">
                    <input type="text" name="search" value="{{ request.GET.search|default:'' }}" placeholder="Search event name..." class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none focus:border-indigo-500">
                </div>
                <div class="w-48">
                    <label class="block text-xs text-gray-500 mb-1">Event Type</label>
                    <select name="type" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none bg-white">
                        <option value="">All</option>
                        <option value="Performance" {% if request.GET.type == 'Performance' %}selected{% endif %}>Performance</option>
                        <option value="Competition" {% if request.GET.type == 'Competition' %}selected{% endif %}>Competition</option>
                        <option value="Workshop" {% if request.GET.type == 'Workshop' %}selected{% endif %}>Workshop</option>
                        <option value="Masterclass" {% if request.GET.type == 'Masterclass' %}selected{% endif %}>Masterclass</option>
                        <option value="Audition" {% if request.GET.type == 'Audition' %}selected{% endif %}>Audition</option>
                        <option value="Meeting" {% if request.GET.type == 'Meeting' %}selected{% endif %}>Meeting</option>
                        <option value="Other" {% if request.GET.type == 'Other' %}selected{% endif %}>Other</option>
                    </select>
                </div>
                <div class="w-48">
                    <label class="block text-xs text-gray-500 mb-1">Status</label>
                    <select name="status" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none bg-white">
                        <option value="">All</option>
                        <option value="1" {% if request.GET.status == '1' %}selected{% endif %}>Upcoming</option>
                        <option value="2" {% if request.GET.status == '2' %}selected{% endif %}>Completed</option>
                        <option value="3" {% if request.GET.status == '3' %}selected{% endif %}>Cancelled</option>
                    </select>
                </div>
                <div class="w-40">
                    <label class="block text-xs text-gray-500 mb-1">From Date</label>
                    <input type="date" name="from_date" value="{{ request.GET.from_date|default:'' }}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none text-gray-500">
                </div>
                <div class="w-40">
                    <label class="block text-xs text-gray-500 mb-1">To Date</label>
                    <input type="date" name="to_date" value="{{ request.GET.to_date|default:'' }}" class="w-full border border-gray-300 rounded px-3 py-2 text-sm outline-none text-gray-500">
                </div>
                <div class="flex space-x-2">
                    <button type="submit" class="bg-[#4f46e5] text-white px-5 py-2 rounded text-sm shadow-sm flex items-center hover:bg-indigo-700">
                        <i class="fa-solid fa-filter mr-1.5"></i> Filter
                    </button>
                    <a href="{% url 'events_dashboard' %}?tab=list" class="border border-gray-300 text-gray-700 px-3 py-2 rounded text-sm hover:bg-gray-50 flex items-center justify-center">
                        <i class="fa-solid fa-rotate-right"></i>
                    </a>
                </div>
            </form>"""

content = re.sub(pattern, new_filter_block, content, flags=re.DOTALL)

with open('templates/website/events_dashboard.html', 'w') as f:
    f.write(content)
