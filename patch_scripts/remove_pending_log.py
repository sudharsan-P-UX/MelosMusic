import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_log_qs = "leave_qs = LeaveRequest.objects.select_related('user').all()"
new_log_qs = "leave_qs = LeaveRequest.objects.select_related('user').exclude(manager_approval_status='Pending')"

content = content.replace(old_log_qs, new_log_qs)

with open('website/views.py', 'w') as f:
    f.write(content)

with open('templates/website/attendance_log.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# remove 'Pending' from dropdown in attendance_log
old_options = """<option value="">All Statuses</option>
                    <option value="Pending" {% if request.GET.filter_status == 'Pending' %}selected{% endif %}>Pending</option>
                    <option value="Approved" {% if request.GET.filter_status == 'Approved' %}selected{% endif %}>Approved</option>
                    <option value="Rejected" {% if request.GET.filter_status == 'Rejected' %}selected{% endif %}>Rejected</option>"""
                    
new_options = """<option value="">All Statuses</option>
                    <option value="Approved" {% if request.GET.filter_status == 'Approved' %}selected{% endif %}>Approved</option>
                    <option value="Rejected" {% if request.GET.filter_status == 'Rejected' %}selected{% endif %}>Rejected</option>"""

html_content = html_content.replace(old_options, new_options)

with open('templates/website/attendance_log.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
