import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

view_code = """
def audit_logs_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    from users.models import User, UserLoginDetails
    from django.db.models import Q
    from datetime import datetime
    
    users = User.objects.all()
    
    audit_user = request.GET.get('audit_user', '')
    audit_status = request.GET.get('audit_status', '')
    audit_from = request.GET.get('audit_from', '')
    audit_to = request.GET.get('audit_to', '')
    
    audit_qs = UserLoginDetails.objects.select_related('user').order_by('-login_date')
    
    if audit_user:
        audit_qs = audit_qs.filter(user_id=audit_user)
        
    if audit_status:
        audit_qs = audit_qs.filter(remarks__icontains=audit_status)
        
    if audit_from:
        try:
            from_dt = datetime.strptime(audit_from, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__gte=from_dt)
        except: pass
        
    if audit_to:
        try:
            to_dt = datetime.strptime(audit_to, '%Y-%m-%d').date()
            audit_qs = audit_qs.filter(login_date__date__lte=to_dt)
        except: pass

    audit_logs = audit_qs[:100]
    
    return render(request, 'website/audit_logs.html', {
        'page_title': 'Audit Logs',
        'users': users,
        'audit_logs': audit_logs
    })
"""

text += view_code

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
