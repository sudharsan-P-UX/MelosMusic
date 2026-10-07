with open('website/views.py', 'r') as f:
    content = f.read()

new_view = '''
def reports_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    from academics.models import Course, Batch
    from users.models import User
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    return render(request, 'website/reports.html', {
        'user': user,
        'page_title': 'Reports',
        'students': students,
        'courses': courses,
        'batches': batches
    })
'''

if 'def reports_view' not in content:
    content += '\n' + new_view

with open('website/views.py', 'w') as f:
    f.write(content)
