with open('website/views.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.strip() == "if action == 'add_course':":
        lines[i] = '        ' + line.lstrip()
with open('website/views.py', 'w') as f:
    f.writelines(lines)
