import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Add pb-24 to the container of the menu table
old_menu_tab = """    <!-- Menu Details Tab -->
    <div x-show="tab === 'menu'" x-transition class="space-y-4" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">"""
            
new_menu_tab = """    <!-- Menu Details Tab -->
    <div x-show="tab === 'menu'" x-transition class="space-y-4" style="display: none;">
        <div class="bg-white rounded border border-gray-200 shadow-sm pb-24">
            <div class="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">"""

content = content.replace(old_menu_tab, new_menu_tab)

# 2. Remove the empty rows
empty_row_pattern = re.compile(r'<!-- Empty row so the floating save button doesn\'t overlap the last item -->\s*<tr class="h-20 bg-transparent border-t-0">\s*<td colspan="5"></td>\s*</tr>')
content = empty_row_pattern.sub('', content)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
