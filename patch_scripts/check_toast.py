import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# The old toast block starts at <!-- Toast Messages -->
start_idx = content.find('    <!-- Toast Messages -->')
if start_idx != -1:
    end_idx = content.find('</body>', start_idx)
    # But wait, there might be script tags inside it for the old toast.
    old_toast_block = content[start_idx:end_idx]
    
    # Let's see what the exact old toast block contains
    print(old_toast_block)
