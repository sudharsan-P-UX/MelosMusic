import re

with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """
def attendance_log_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    from users.models import User
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except User.DoesNotExist:
        return redirect('login')
        
    tab = request.GET.get('tab', 'students')
    
    # Filter
    filter_status = request.GET.get('filter_status', '')
    filter_from = request.GET.get('filter_from', '')
    filter_to = request.GET.get('filter_to', '')
    
    from academics.models import LeaveRequest
    
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
        'page_title': 'Attendance Log',
        'user': user,
        'tab': tab,
        'leaves': leaves,
    }
    return render(request, 'website/attendance_log.html', context)
"""

content += new_view

with open('website/views.py', 'w') as f:
    f.write(content)
