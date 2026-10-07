with open('website/views.py', 'r') as f:
    content = f.read()

new_views = '''
def pending_fees_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/pending_fees.html', {
        'user': user,
        'page_title': 'Pending Fees'
    })

def receipts_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/receipts.html', {
        'user': user,
        'page_title': 'Receipts'
    })

def refunds_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    return render(request, 'website/refunds.html', {
        'user': user,
        'page_title': 'Refunds'
    })
'''

if 'def pending_fees_view' not in content:
    content += '\n' + new_views

with open('website/views.py', 'w') as f:
    f.write(content)
