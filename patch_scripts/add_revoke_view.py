import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_view = """def attendance_log_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    from users.models import User
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        return redirect('login')
        
    tab = request.GET.get('tab', 'students')"""

new_view = """def attendance_log_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    from users.models import User
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        return redirect('login')
        
    from academics.models import LeaveRequest
    
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('leave_request_id')
        if action == 'Revoke' and request_id:
            lr = LeaveRequest.objects.get(leave_request_id=request_id)
            lr.manager_approval_status = 'Pending'
            lr.manager_approval_on = None
            lr.save()
            messages.success(request, 'Request revoked and moved back to approvals!')
        return redirect(f'/attendance-log/?tab={request.GET.get("tab", "students")}')
        
    tab = request.GET.get('tab', 'students')"""

content = content.replace(old_view, new_view)

with open('website/views.py', 'w') as f:
    f.write(content)
