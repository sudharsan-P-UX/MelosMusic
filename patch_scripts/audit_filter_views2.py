import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_audit = """    from users.models import UserLoginDetails
    from django.db.models import Q
    audit_search = request.GET.get('audit_search', '')
    audit_qs = UserLoginDetails.objects.select_related('user').order_by('-login_date')
    if audit_search:
        audit_qs = audit_qs.filter(
            Q(user__display_name__icontains=audit_search) |
            Q(user__first_name__icontains=audit_search) |
            Q(user__last_name__icontains=audit_search) |
            Q(remarks__icontains=audit_search)
        )
    audit_logs = audit_qs[:50]"""

new_audit = """    from users.models import UserLoginDetails
    from django.db.models import Q
    from datetime import datetime
    
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

    audit_logs = audit_qs[:100]"""

content = content.replace(old_audit, new_audit)

with open('website/views.py', 'w') as f:
    f.write(content)
