import re

with open('templates/website/courses_batches.html', 'r') as f:
    content = f.read()

# 1. Update x-data
old_xdata = '<div x-data="{ tab: \'courses\', showCourseModal: false, showBatchModal: false }">'
new_xdata = '<div x-data="courseBatchData()">'

content = content.replace(old_xdata, new_xdata)

# 2. Update select
old_select = """<select name="course_id" required class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                                    <option value="">-- Select Course --</option>
                                    {% for course in courses %}
                                    <option value="{{ course.course_id }}">{{ course.course_name }}</option>
                                    {% endfor %}
                                </select>"""

new_select = """<select name="course_id" required x-model="selectedCourseId" @change="calculateEndDate" id="batch_course_select" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">
                                    <option value="" data-duration="0">-- Select Course --</option>
                                    {% for course in courses %}
                                    <option value="{{ course.course_id }}" data-duration="{{ course.duration_months|default:0 }}">{{ course.course_name }}</option>
                                    {% endfor %}
                                </select>"""

content = content.replace(old_select, new_select)

# 3. Update inputs
old_start = '<input type="date" name="start_date" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'
new_start = '<input type="date" name="start_date" x-model="startDate" @change="calculateEndDate" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'

old_end = '<input type="date" name="end_date" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'
new_end = '<input type="date" name="end_date" x-model="endDate" class="w-full border border-gray-300 rounded-md px-3 py-2 outline-none focus:ring-1 focus:ring-indigo-500 text-sm">'

content = content.replace(old_start, new_start)
content = content.replace(old_end, new_end)

# 4. Add script block at the end
script = """
<script>
function courseBatchData() {
    return {
        tab: 'courses',
        showCourseModal: false,
        showBatchModal: false,
        selectedCourseId: '',
        startDate: '',
        endDate: '',
        
        calculateEndDate() {
            if (!this.startDate || !this.selectedCourseId) return;
            
            const select = document.getElementById('batch_course_select');
            if(!select) return;
            const option = select.options[select.selectedIndex];
            if(!option) return;
            
            const durationMonths = parseInt(option.getAttribute('data-duration')) || 0;
            if(durationMonths === 0) return;
            
            const start = new Date(this.startDate);
            if(isNaN(start.getTime())) return;
            
            // Add months
            start.setMonth(start.getMonth() + durationMonths);
            
            // Format to YYYY-MM-DD
            const yyyy = start.getFullYear();
            const mm = String(start.getMonth() + 1).padStart(2, '0');
            const dd = String(start.getDate()).padStart(2, '0');
            this.endDate = `${yyyy}-${mm}-${dd}`;
        }
    }
}
</script>
"""

if "function courseBatchData" not in content:
    content = content.replace('{% endblock %}', script + '\n{% endblock %}')

with open('templates/website/courses_batches.html', 'w') as f:
    f.write(content)
