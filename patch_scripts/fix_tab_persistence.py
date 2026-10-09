import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Update attendance_log_view redirect
old_log_redirect = """        return redirect(f'/attendance-log/?tab={request.GET.get("tab", "students")}')"""
new_log_redirect = """        return redirect(f'/attendance-log/?tab={request.POST.get("tab", request.GET.get("tab", "students"))}')"""
content = content.replace(old_log_redirect, new_log_redirect)

# Update attendance_approval_view redirect
old_app_redirect = """        return redirect(f'/attendance-approval/?tab={request.GET.get("tab", "students")}')"""
new_app_redirect = """        return redirect(f'/attendance-approval/?tab={request.POST.get("tab", request.GET.get("tab", "students"))}')"""
content = content.replace(old_app_redirect, new_app_redirect)

with open('website/views.py', 'w') as f:
    f.write(content)

with open('templates/website/attendance_log.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add hidden tab input
html_content = html_content.replace('<input type="hidden" name="leave_request_id"', '<input type="hidden" name="tab" value="{{ tab }}">\n                                <input type="hidden" name="leave_request_id"')

with open('templates/website/attendance_log.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('templates/website/attendance_approval.html', 'r', encoding='utf-8') as f:
    html_content2 = f.read()

html_content2 = html_content2.replace('<input type="hidden" name="leave_request_id"', '<input type="hidden" name="tab" value="{{ tab }}">\n                                <input type="hidden" name="leave_request_id"')

with open('templates/website/attendance_approval.html', 'w', encoding='utf-8') as f:
    f.write(html_content2)
