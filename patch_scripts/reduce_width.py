import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Limit the max width of the whole roles tab content
content = content.replace(
    '<div x-show="tab === \'roles\'" x-transition class="space-y-6">',
    '<div x-show="tab === \'roles\'" x-transition class="space-y-6 max-w-5xl">'
)

# 2. Make the role matrix header sticky
old_matrix_header = """        <!-- Role Matrix Editor -->
        <div class="bg-white rounded border border-gray-200 shadow-sm">
            <div class="p-5 border-b border-gray-200 bg-gray-50 flex justify-between items-center">"""

new_matrix_header = """        <!-- Role Matrix Editor -->
        <div class="bg-white rounded border border-gray-200 shadow-sm relative">
            <div class="p-5 border-b border-gray-200 bg-gray-50/90 backdrop-blur-md flex justify-between items-center sticky top-0 z-30 rounded-t shadow-sm">"""

content = content.replace(old_matrix_header, new_matrix_header)

# 3. Fix the table header so it sticks underneath the matrix header
# The matrix header is p-5 (1.25rem * 2 = 2.5rem = 40px) + h3 (1.5rem = 24px) + p (1rem = 16px) ~= 80px tall.
# top-[85px] is a good estimate.
old_thead = '<tr class="border-b-2 border-gray-200 text-gray-600 bg-gray-50/90 backdrop-blur sticky top-0 z-10 shadow-sm">'
new_thead = '<tr class="border-b-2 border-gray-200 text-gray-600 bg-gray-50/95 backdrop-blur-md sticky top-[82px] z-20 shadow-sm">'

content = content.replace(old_thead, new_thead)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
