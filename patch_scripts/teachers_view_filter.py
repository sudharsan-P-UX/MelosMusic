import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_logic = """    teachers = User.objects.filter(role=teacher_role).order_by('-user_id')
        
    return render(request, 'website/teachers.html', {"""

new_logic = """    teachers = User.objects.filter(role=teacher_role).order_by('-user_id')
    
    # Filter logic for teachers
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status_filter', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    from django.db.models import Q
    
    if search:
        teachers = teachers.filter(
            Q(display_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(phone__icontains=search) |
            Q(user_code__icontains=search)
        )
        
    if status_filter != '':
        teachers = teachers.filter(is_active=(status_filter == '1'))
        
    if from_date:
        teachers = teachers.filter(created_date__gte=from_date)
        
    if to_date:
        teachers = teachers.filter(created_date__lte=to_date)
        
    return render(request, 'website/teachers.html', {"""

content = content.replace(old_logic, new_logic)

with open('website/views.py', 'w') as f:
    f.write(content)
