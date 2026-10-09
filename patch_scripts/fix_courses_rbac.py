import re

with open('website/views.py', 'r') as f:
    content = f.read()

# We need to target the block specifically inside courses_batches_view
pattern = r"(def courses_batches_view\(request\):.*?if request\.method == 'POST':\s*action = request\.POST\.get\('action'\)\s*)(.*?)(        if action == 'add_course':)"

def fix_courses_view(match):
    prefix = match.group(1)
    bad_code = match.group(2)
    suffix = match.group(3)
    
    # Check if the bad code contains admin_access.
    # If it does, we just return prefix + suffix, effectively deleting the bad code block.
    if 'admin_access' in bad_code:
        return prefix + suffix
    else:
        return match.group(0)

new_content = re.sub(pattern, fix_courses_view, content, flags=re.DOTALL)

with open('website/views.py', 'w') as f:
    f.write(new_content)
