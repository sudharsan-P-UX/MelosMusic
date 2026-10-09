import re

def wrap_button(file_path, btn_pattern):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replace
    new_content = re.sub(
        r'(<button[^>]*?' + btn_pattern + r'[^>]*?>.*?</button>)', 
        r'{% if menu_access.add %}\1{% endif %}', 
        content, 
        flags=re.DOTALL
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def wrap_link(file_path, btn_pattern):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replace
    new_content = re.sub(
        r'(<a[^>]*?' + btn_pattern + r'[^>]*?>.*?</a>)', 
        r'{% if menu_access.add %}\1{% endif %}', 
        content, 
        flags=re.DOTALL
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def wrap_div_or_button(file_path, text_to_replace, wrapper_open='{% if menu_access.add %}', wrapper_close='{% endif %}'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(text_to_replace, wrapper_open + text_to_replace + wrapper_close)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Students: "Quick Add Student"
student_btn = """<button type="button" onclick="openModal()" class="bg-[#0066cc] hover:bg-blue-700 text-white font-medium py-1.5 px-4 rounded shadow-sm text-sm h-[34px] flex items-center">
                    <i class="fa-solid fa-plus mr-1.5"></i> Quick Add Student
                </button>"""
wrap_div_or_button('templates/website/students.html', student_btn)

# Teachers: "Add Teacher"
teacher_btn = """<button type="button" onclick="openModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-1.5 px-4 rounded shadow-sm text-sm h-[34px] flex items-center">
                    <i class="fa-solid fa-plus mr-1.5"></i> Add Teacher
                </button>"""
wrap_div_or_button('templates/website/teachers.html', teacher_btn)

# Courses & Batches: "Add Course", "Add Batch"
course_btn = """<button @click="showCourseModal = true" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Add Course
            </button>"""
wrap_div_or_button('templates/website/courses_batches.html', course_btn)

batch_btn = """<button @click="showBatchModal = true" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Add Batch
            </button>"""
wrap_div_or_button('templates/website/courses_batches.html', batch_btn)

# Enrollment Management: "Assign to Course"
assign_btn = """<button type="button" onclick="document.getElementById('assignModal').classList.remove('hidden'); document.getElementById('assignModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-1.5 px-4 rounded shadow-sm text-sm h-[34px] flex items-center">
                    <i class="fa-solid fa-user-plus mr-1.5"></i> Assign to Course
                </button>"""
wrap_div_or_button('templates/website/enrollment_management.html', assign_btn)

# Student Course Allocation
student_alloc_btn = """<button type="button" onclick="document.getElementById('allocationModal').classList.remove('hidden'); document.getElementById('allocationModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Allocate Course
            </button>"""
wrap_div_or_button('templates/website/student_course_allocation.html', student_alloc_btn)

# Teacher Class Allocation
teacher_alloc_btn = """<button type="button" onclick="document.getElementById('allocationModal').classList.remove('hidden'); document.getElementById('allocationModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Allocate Teacher
            </button>"""
wrap_div_or_button('templates/website/teacher_class_allocation.html', teacher_alloc_btn)

# Student Attendance / Teacher Attendance
s_att_btn = """<button type="button" onclick="document.getElementById('attendanceModal').classList.remove('hidden'); document.getElementById('attendanceModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Add Attendance
            </button>"""
s_req_btn = """<button type="button" onclick="document.getElementById('leaveModal').classList.remove('hidden'); document.getElementById('leaveModal').classList.add('flex')" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-paper-plane mr-2"></i> Attendance Request
            </button>"""
wrap_div_or_button('templates/website/student_attendance.html', s_att_btn)
wrap_div_or_button('templates/website/student_attendance.html', s_req_btn)
wrap_div_or_button('templates/website/teacher_attendance.html', s_att_btn)
wrap_div_or_button('templates/website/teacher_attendance.html', s_req_btn)

print("Buttons wrapped successfully!")
