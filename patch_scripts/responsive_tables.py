import os
import re

# 1. Fix base.html header
with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<span class="text-sm font-medium text-gray-500">Welcome, {{ user.first_name }}</span>',
    '<span class="hidden md:inline-block text-sm font-medium text-gray-500">Welcome, {{ user.first_name }}</span>'
)
text = text.replace(
    '<div class="flex items-center space-x-4">',
    '<div class="flex items-center space-x-2 md:space-x-4">'
)
text = text.replace(
    'ml-4 font-bold border border-red-200',
    'ml-2 md:ml-4 font-bold border border-red-200'
)
# Shrink Dashboard header on mobile to prevent overlapping
text = text.replace(
    '<h1 class="text-xl font-semibold text-gray-800 truncate max-w-[200px] md:max-w-none">',
    '<h1 class="text-lg md:text-xl font-semibold text-gray-800 truncate max-w-[120px] md:max-w-none">'
)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Fix all tables in all templates
template_dirs = ['templates', 'website/templates']
for root, dirs, files in os.walk('.'):
    if 'templates' in root:
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it contains a table that isn't already wrapped in overflow-x-auto
                # A simple regex to wrap <table> tags
                # To avoid double wrapping, we can first remove existing simple wrappers, or just use a specific class
                
                # We'll just do a targeted replace for typical table starts
                new_content = re.sub(r'(?<!<div class="overflow-x-auto w-full">)(\s*)<table', r'\1<div class="overflow-x-auto w-full">\n\1<table', content)
                new_content = re.sub(r'</table>(\s*)(?!</div>)', r'</table>\n\1</div>', new_content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
