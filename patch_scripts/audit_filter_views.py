import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_audit = """    from users.models import UserLoginDetails
    audit_logs = UserLoginDetails.objects.select_related('user').order_by('-login_date')[:50]"""

new_audit = """    from users.models import UserLoginDetails
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

content = content.replace(old_audit, new_audit)

with open('website/views.py', 'w') as f:
    f.write(content)
