import re

with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """
def attendance_approval_view(request):
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
        if action in ['Approve', 'Reject'] and request_id:
            from django.utils import timezone
            lr = LeaveRequest.objects.get(leave_request_id=request_id)
            lr.manager_approval_status = 'Approved' if action == 'Approve' else 'Rejected'
            lr.manager_approval_on = timezone.now()
            lr.save()
            messages.success(request, f'Request {action}d successfully!')
        return redirect(f'/attendance-approval/?tab={request.GET.get("tab", "students")}')
        
    tab = request.GET.get('tab', 'students')
    filter_status = request.GET.get('filter_status', 'Pending') # Default to pending for approvals
    filter_from = request.GET.get('filter_from', '')
    filter_to = request.GET.get('filter_to', '')
    
    leave_qs = LeaveRequest.objects.select_related('user').all()
    
    if tab == 'students':
        leave_qs = leave_qs.filter(user_type='Student')
    else:
        leave_qs = leave_qs.filter(user_type='Teacher')
        
    if filter_status:
        leave_qs = leave_qs.filter(manager_approval_status=filter_status)
    if filter_from:
        try:
            leave_qs = leave_qs.filter(from_date__gte=filter_from)
        except: pass
    if filter_to:
        try:
            leave_qs = leave_qs.filter(to_date__lte=filter_to)
        except: pass
        
    leaves = leave_qs.order_by('-applied_date')

    context = {
        'page_title': 'Attendance Approval',
        'user': user,
        'tab': tab,
        'leaves': leaves,
    }
    return render(request, 'website/attendance_approval.html', context)
"""

content += new_view

with open('website/views.py', 'w') as f:
    f.write(content)
