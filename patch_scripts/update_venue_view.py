import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_func_def = """def events_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    
    from events.models import EventMaster, EventParticipant, EventVenue, EventAttendance"""

new_func_def = """def events_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    
    from events.models import EventMaster, EventParticipant, EventVenue, EventAttendance
    from django.contrib import messages
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_venue':
            venue_name = request.POST.get('venue_name')
            capacity = request.POST.get('capacity')
            address = request.POST.get('address')
            
            capacity_val = capacity if capacity else None
            
            EventVenue.objects.create(
                venue_name=venue_name,
                capacity=capacity_val,
                address=address
            )
            messages.success(request, 'Venue added successfully!')
            return redirect('/events/?tab=venue')"""

content = content.replace(old_func_def, new_func_def)

with open('website/views.py', 'w') as f:
    f.write(content)
