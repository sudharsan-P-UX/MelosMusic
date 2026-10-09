import re

with open('website/views.py', 'r') as f:
    content = f.read()

# We want attendance_log_view to EXCLUDE Pending.
# We want attendance_approval_view to NOT exclude Pending (i.e. .all())

def fix_views(text):
    log_pattern = re.compile(r'(def attendance_log_view.*?)(leave_qs = LeaveRequest\.objects\.select_related\(\'user\'\)\.[^\n]+)(.*?)def attendance_approval_view', re.DOTALL)
    
    app_pattern = re.compile(r'(def attendance_approval_view.*?)(leave_qs = LeaveRequest\.objects\.select_related\(\'user\'\)\.[^\n]+)(.*)', re.DOTALL)
    
    # fix log view
    text = log_pattern.sub(r"\1leave_qs = LeaveRequest.objects.select_related('user').exclude(manager_approval_status='Pending')\3def attendance_approval_view", text)
    
    # fix app view
    text = app_pattern.sub(r"\1leave_qs = LeaveRequest.objects.select_related('user').all()\3", text)
    
    return text

content = fix_views(content)

with open('website/views.py', 'w') as f:
    f.write(content)
