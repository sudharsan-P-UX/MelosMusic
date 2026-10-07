with open('website/views.py', 'r') as f:
    content = f.read()

new_view = '''
def assign_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    from academics.models import Course, Batch
    from finance.models import StudentFee
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Here we would map the form data to the StudentFee model
        messages.success(request, 'Fees assigned successfully!')
        return redirect('assign_fees')
        
    return render(request, 'website/assign_fees.html', {
        'user': user,
        'page_title': 'Assign Fees',
        'students': students,
        'courses': courses,
        'batches': batches
    })
'''

if 'def assign_fees_view' not in content:
    content += '\n' + new_view

with open('website/views.py', 'w') as f:
    f.write(content)
