import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Restore the width by removing max-w-5xl
content = content.replace(
    '<div x-show="tab === \'roles\'" x-transition class="space-y-6 max-w-5xl">',
    '<div x-show="tab === \'roles\'" x-transition class="space-y-6">'
)

# 2. Reduce padding in the matrix header
content = content.replace(
    '<div class="p-5 border-b border-gray-200 bg-gray-50/90 backdrop-blur-md flex justify-between items-center sticky top-0 z-30 rounded-t shadow-sm">',
    '<div class="py-3 px-4 border-b border-gray-200 bg-gray-50/90 backdrop-blur-md flex justify-between items-center sticky top-0 z-30 rounded-t shadow-sm">'
)

# 3. Reduce the top margin in the text
content = content.replace(
    '<p class="text-xs text-gray-500 mt-1">Select a role to configure access</p>',
    '<p class="text-xs text-gray-500 mt-0.5">Select a role to configure access</p>'
)

# 4. Reduce padding in the role description body
content = content.replace(
    '<div class="p-6">',
    '<div class="py-2 px-4">'
)

# 5. Reduce bottom margin on the role description
content = content.replace(
    '<div class="mb-6">',
    '<div class="mb-3">'
)

# Also fix the sticky top offset for the table header now that the matrix header is shorter
# It was top-[82px]. New height: py-3 (0.75*2 = 1.5rem = 24px) + h3 (1.5rem = 24px) + p (1rem = 16px) = ~64px
content = content.replace(
    'top-[82px]',
    'top-[56px]'
)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
