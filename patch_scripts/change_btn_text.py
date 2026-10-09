import re

with open('templates/website/student_allocation.html', 'r') as f:
    content = f.read()

# Replace button text
content = content.replace(
    '<i class="fa-solid fa-plus mr-2"></i> Add Student',
    '<i class="fa-solid fa-plus mr-2"></i> Add Std Allocation'
)

with open('templates/website/student_allocation.html', 'w') as f:
    f.write(content)
