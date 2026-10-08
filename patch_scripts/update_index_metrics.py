import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_index = """def index(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Fetch user for dashboard display
    user = User.objects.get(user_id=request.session['user_id'])
    return render(request, 'website/index.html', {'user': user})"""

new_index = """from academics.models import Course
from finance.models import StudentFeeInstallment
from django.db.models import Sum, F

def index(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Fetch user for dashboard display
    user = User.objects.get(user_id=request.session['user_id'])
    
    # Dashboard metrics
    total_students = User.objects.filter(role__role_name__iexact='student').count()
    active_teachers = User.objects.filter(role__role_name__iexact='teacher').count()
    total_courses = Course.objects.filter(is_active=True).count()
    
    pending_fees = StudentFeeInstallment.objects.filter(amount__gt=F('paid_amount')).aggregate(
        total_pending=Sum(F('amount') - F('paid_amount'))
    )['total_pending'] or 0
    
    context = {
        'user': user,
        'total_students': total_students,
        'active_teachers': active_teachers,
        'total_courses': total_courses,
        'pending_fees': pending_fees,
    }
    return render(request, 'website/index.html', context)"""

content = content.replace(old_index, new_index)

with open('website/views.py', 'w') as f:
    f.write(content)
