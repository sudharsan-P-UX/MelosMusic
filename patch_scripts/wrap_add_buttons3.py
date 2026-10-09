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

add_user_btn = """<button @click="showAddUserModal = true" class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-user-plus mr-1"></i> Add User
                </button>"""
                
create_role_btn = """<button @click="showAddRoleModal = true" class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-shield-plus mr-1"></i> Create Role
                </button>"""
                
add_menu_btn = """<button @click="showAddMenuModal = true" class="bg-[#4f46e5] text-white px-4 py-1.5 rounded text-xs font-medium hover:bg-indigo-700 transition">
                    <i class="fa-solid fa-folder-plus mr-1"></i> Add Menu
                </button>"""
                
wrap_div_or_button('templates/website/admin_dashboard.html', add_user_btn)
wrap_div_or_button('templates/website/admin_dashboard.html', create_role_btn)
wrap_div_or_button('templates/website/admin_dashboard.html', add_menu_btn)
