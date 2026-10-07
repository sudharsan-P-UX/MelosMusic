import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

old_btn_container = """                    <div class="mt-6 flex justify-end">
                        <button type="submit" class="bg-[#4f46e5] text-white px-6 py-2 rounded text-sm font-medium hover:bg-indigo-700 transition shadow-sm">
                            <i class="fa-solid fa-check mr-2"></i> Save Role
                        </button>
                    </div>"""

new_btn_container = """                    <div class="sticky bottom-0 -mx-6 -mb-6 p-4 bg-white/95 backdrop-blur-sm border-t border-gray-200 flex justify-end shadow-[0_-10px_15px_-3px_rgba(0,0,0,0.05)] rounded-b-lg z-20 mt-6">
                        <button type="submit" class="bg-[#4f46e5] text-white px-8 py-2.5 rounded shadow text-sm font-medium hover:bg-indigo-700 transition-all transform hover:scale-[1.02]">
                            <i class="fa-solid fa-check mr-2"></i> Save Role
                        </button>
                    </div>"""

content = content.replace(old_btn_container, new_btn_container)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
