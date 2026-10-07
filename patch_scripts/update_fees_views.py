with open('website/views.py', 'r') as f:
    content = f.read()

new_view = '''
def fee_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(user_id=request.session['user_id'])
    
    # We will just pass mock data for the dashboard for now since we just created the DB
    return render(request, 'website/fee_dashboard.html', {
        'user': user,
        'page_title': 'Fee Dashboard',
        'todays_collection': '15,000',
        'monthly_collection': '1,25,000',
        'pending_fees': '45,000',
        'overdue_fees': '12,000',
        'students_paid': '80',
        'students_pending': '20'
    })
'''
if 'def fee_dashboard_view' not in content:
    content += '\n' + new_view

with open('website/views.py', 'w') as f:
    f.write(content)
