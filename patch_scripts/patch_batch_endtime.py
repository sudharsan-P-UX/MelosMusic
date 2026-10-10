import os
import re

def patch_courses_html():
    with open('templates/website/courses_batches.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add data-duration-hrs to options
    content = content.replace(
        """data-duration="{{ course.duration_months|default:0 }}">{{ course.course_name }}</option>""",
        """data-duration="{{ course.duration_months|default:0 }}" data-duration-hrs="{{ course.duration_hrs|default:0 }}">{{ course.course_name }}</option>"""
    )
    content = content.replace(
        """data-duration="0">-- Select Course --</option>""",
        """data-duration="0" data-duration-hrs="0">-- Select Course --</option>"""
    )
    
    # 2. Update select tag to call calculateEndTime as well
    content = content.replace(
        """@change="calculateEndDate" id="batch_course_select" """,
        """@change="calculateEndDate(); calculateEndTime()" id="batch_course_select" """
    )
    
    # 3. Bind startTime and endTime
    content = content.replace(
        """<input type="time" name="start_time" class="w-full""",
        """<input type="time" name="start_time" x-model="startTime" @change="calculateEndTime" class="w-full"""
    )
    content = content.replace(
        """<input type="time" name="end_time" class="w-full""",
        """<input type="time" name="end_time" x-model="endTime" class="w-full"""
    )
    
    # 4. Update x-data object
    if "startTime: ''," not in content:
        content = content.replace(
            "endDate: '',",
            "endDate: '',\n        startTime: '',\n        endTime: '',"
        )
    
    # 5. Add calculateEndTime function
    func = """
        calculateEndTime() {
            if (!this.startTime || !this.selectedCourseId) return;
            const select = document.getElementById('batch_course_select');
            if(!select) return;
            const option = select.options[select.selectedIndex];
            if(!option) return;
            const durationHrs = parseFloat(option.getAttribute('data-duration-hrs')) || 0;
            if(durationHrs === 0) return;
            
            // Create a dummy date with the start time
            const d = new Date(`1970-01-01T${this.startTime}`);
            if(isNaN(d.getTime())) return;
            
            // Add hours (durationHrs * 60 minutes)
            d.setMinutes(d.getMinutes() + (durationHrs * 60));
            
            // Extract the new time (HH:MM)
            const hh = String(d.getHours()).padStart(2, '0');
            const mm = String(d.getMinutes()).padStart(2, '0');
            this.endTime = `${hh}:${mm}`;
        },"""
    
    if "calculateEndTime()" not in content:
        content = content.replace(
            "calculateEndDate() {",
            func + "\n        calculateEndDate() {"
        )

    with open('templates/website/courses_batches.html', 'w', encoding='utf-8') as f:
        f.write(content)

patch_courses_html()
print("Patched Add Batch end time calculation.")
