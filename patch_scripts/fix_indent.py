with open('website/views.py', 'r') as f:
    lines = f.readlines()

new_lines = []
in_admin = False
for line in lines:
    if line.startswith('def admin_dashboard_view(request):'):
        in_admin = True
    
    if in_admin and line.startswith('        if request.method == \'POST\':'):
        # We found the broken block, we need to unindent it by 4 spaces
        new_lines.append(line[4:])
    elif in_admin and line.startswith('        action = request.POST.get(\'action\')'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('        if action == \'create_user\':'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            first_name = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            last_name = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            email = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            phone = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            password = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            role_id = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            try:'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                role = '):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                User.objects.create('):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    first_name='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    last_name='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    display_name='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    email='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    phone='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    password='):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                    role=role'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                )'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            except Exception as e:'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('                print(e)'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('            return redirect(\'/admin-dashboard/?tab=users\')'):
        new_lines.append(line[4:])
    elif in_admin and line.startswith('    tab = request.GET.get(\'tab\', \'dashboard\')'):
        new_lines.append(line)
        in_admin = False # End of block
    else:
        new_lines.append(line)

with open('website/views.py', 'w') as f:
    f.writelines(new_lines)
