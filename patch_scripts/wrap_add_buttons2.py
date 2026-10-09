import re

def wrap_div_or_button(file_path, text_to_replace, wrapper_open='{% if menu_access.add %}', wrapper_close='{% endif %}'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already wrapped to avoid double wrapping
    if wrapper_open + text_to_replace in content:
        return
        
    content = content.replace(text_to_replace, wrapper_open + text_to_replace + wrapper_close)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Student Course Allocation
student_alloc_btn = """<button type="button" onclick="document.getElementById('allocationModal').classList.remove('hidden'); document.getElementById('allocationModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Allocate Course
            </button>"""
wrap_div_or_button('templates/website/student_allocation.html', student_alloc_btn)

# Teacher Class Allocation
teacher_alloc_btn = """<button type="button" onclick="document.getElementById('allocationModal').classList.remove('hidden'); document.getElementById('allocationModal').classList.add('flex')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md font-medium transition shadow-sm flex items-center text-sm">
                <i class="fa-solid fa-plus mr-2"></i> Allocate Teacher
            </button>"""
wrap_div_or_button('templates/website/teacher_allocation.html', teacher_alloc_btn)
