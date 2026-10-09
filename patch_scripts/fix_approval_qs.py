import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Fix the attendance_approval_view qs
old_approval_qs = """    filter_to = request.GET.get('filter_to', '')
    
    leave_qs = LeaveRequest.objects.select_related('user').exclude(manager_approval_status='Pending')
    
    if tab == 'students':"""

new_approval_qs = """    filter_to = request.GET.get('filter_to', '')
    
    leave_qs = LeaveRequest.objects.select_related('user').all()
    
    if tab == 'students':"""

# we only want to change it inside attendance_approval_view
# the code block matches attendance_approval_view. Let's make sure it doesn't break log_view
content = content.replace(old_approval_qs, new_approval_qs, 1)

with open('website/views.py', 'w') as f:
    f.write(content)
