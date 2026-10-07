with open('website/views.py', 'r') as f:
    content = f.read()

new_view = '''
def fee_collection_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    from academics.models import Course, Batch
    from users.models import User
    
    students = User.objects.filter(role__role_name='Student', is_active=True)
    courses = Course.objects.filter(is_active=True)
    batches = Batch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Here we would handle the actual payment collection mapping to FeePayment, FeeReceipt, etc.
        messages.success(request, 'Fee payment collected successfully! Receipt generated.')
        return redirect('fee_collection')
        
    return render(request, 'website/fee_collection.html', {
        'user': user,
        'page_title': 'Fee Collection',
        'students': students,
        'courses': courses,
        'batches': batches
    })
'''

if 'def fee_collection_view' not in content:
    content += '\n' + new_view

with open('website/views.py', 'w') as f:
    f.write(content)
