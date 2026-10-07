with open('website/views.py', 'r') as f:
    content = f.read()

import re

new_view = """def create_event_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        from events.models import EventMaster, EventVenue
        from users.models import User
        
        user = User.objects.get(user_id=request.session['user_id'])
        
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        status = request.POST.get('status')
        description = request.POST.get('description')
        
        venue = None
        if venue_id and venue_id != '0':
            try:
                venue = EventVenue.objects.get(venue_id=venue_id)
            except:
                pass
                
        EventMaster.objects.create(
            event_name=event_name,
            event_type=event_type,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            status=status,
            description=description,
            created_by=user
        )
        
        from django.contrib import messages
        messages.success(request, 'Event added successfully!')
        
        return redirect('/events/?tab=upcoming')
        
    return redirect('/events/?tab=create')

def generic_page"""

content = content.replace('def generic_page', new_view)

with open('website/views.py', 'w') as f:
    f.write(content)
