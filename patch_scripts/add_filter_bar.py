import re

with open('templates/website/student_course.html', 'r') as f:
    content = f.read()

filter_bar = """
    <!-- Filter Bar -->
    <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <form method="GET" action="{% url 'student_course' %}" class="flex flex-wrap gap-4 items-end">
            <div class="relative">
                <input type="text" name="search" value="{{ request.GET.search|default:'' }}" placeholder="Search Student or Course" class="border border-gray-300 rounded px-3 py-1.5 w-64 text-sm focus:outline-none focus:border-indigo-500 h-[36px]">
                <i class="fa-solid fa-magnifying-glass absolute right-3 top-2.5 text-gray-400"></i>
            </div>
            <div class="w-48">
                <select name="course_id" class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm text-gray-700 outline-none h-[36px]">
                    <option value="">All Courses</option>
                    {% for c in courses %}
                    <option value="{{ c.course_id }}" {% if request.GET.course_id == c.course_id|stringformat:"s" %}selected{% endif %}>{{ c.course_name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="flex space-x-2">
                <button type="submit" class="bg-indigo-600 text-white px-4 py-1.5 rounded text-sm hover:bg-indigo-700 h-[36px] flex items-center shadow-sm">
                    <i class="fa-solid fa-filter mr-1.5"></i> Apply
                </button>
                <a href="{% url 'student_course' %}" class="bg-white border border-gray-300 text-gray-600 px-4 py-1.5 rounded text-sm hover:bg-gray-50 h-[36px] flex items-center shadow-sm">
                    Clear
                </a>
            </div>
        </form>
    </div>
"""

# Insert filter bar after the header
content = content.replace(
    '<div class="overflow-x-auto p-0">',
    filter_bar + '\n    <div class="overflow-x-auto p-0">'
)

with open('templates/website/student_course.html', 'w') as f:
    f.write(content)
