import re

with open('templates/website/admin_dashboard.html', 'r') as f:
    content = f.read()

# 1. Reduce the main header bottom margin
content = content.replace(
    '<div class="mb-6 flex justify-between items-center">',
    '<div class="mb-4 flex justify-between items-center">'
)

# 2. Reduce the gap between elements in the Roles tab
content = content.replace(
    '<div x-show="tab === \'roles\'" x-transition class="space-y-6">',
    '<div x-show="tab === \'roles\'" x-transition class="space-y-4">'
)

# 3. Reduce padding inside the Stats cards
content = content.replace(
    '<div class="bg-white p-6 rounded border border-gray-200 shadow-sm flex items-center">',
    '<div class="bg-white p-4 rounded border border-gray-200 shadow-sm flex items-center">'
)

# We should do the same for the other tabs just to be consistent
content = content.replace(
    '<div x-show="tab === \'dashboard\'" x-transition class="space-y-6"',
    '<div x-show="tab === \'dashboard\'" x-transition class="space-y-4"'
)
content = content.replace(
    '<div x-show="tab === \'users\'" x-transition class="space-y-6"',
    '<div x-show="tab === \'users\'" x-transition class="space-y-4"'
)
content = content.replace(
    '<div x-show="tab === \'menu\'" x-transition class="space-y-6"',
    '<div x-show="tab === \'menu\'" x-transition class="space-y-4"'
)
content = content.replace(
    '<div x-show="tab === \'audit\'" x-transition class="space-y-6"',
    '<div x-show="tab === \'audit\'" x-transition class="space-y-4"'
)

with open('templates/website/admin_dashboard.html', 'w') as f:
    f.write(content)
