import os
import re

# 1. Fix Alpine @click closing issue which cancels navigation on mobile webviews
with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('@click="sidebarOpen = false" ', '')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Fix Modal Button Alignment across all templates
template_dirs = ['templates', 'website/templates']
for root, dirs, files in os.walk('.'):
    if 'templates' in root:
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the messy flex layout with a clean grid layout for mobile
                new_content = content.replace(
                    'flex flex-row-reverse rounded-b-lg',
                    'grid grid-cols-2 gap-3 sm:flex sm:flex-row-reverse rounded-b-lg'
                )
                
                # Remove the margin-top that was causing the cancel button to be pushed down
                new_content = new_content.replace('mt-3 w-full', 'w-full')
                new_content = new_content.replace('sm:mt-0 ', '')
                new_content = new_content.replace('sm:ml-3 ', 'sm:gap-0 sm:ml-3 ')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

print("Fixed navigation and button alignments.")
