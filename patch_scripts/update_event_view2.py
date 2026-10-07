with open('website/views.py', 'r') as f:
    content = f.read()

import re

# We need to rewrite create_event_view to capture new fields
old_view = r"def create_event_view\(request\):.*?return redirect\('/events/\?tab=create'\)"

new_view = """def create_event_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        from events.models import EventMaster, EventVenue
        from users.models import User
        
        user = User.objects.get(user_id=request.session['user_id'])
        
        event_id = request.POST.get('event_id') # For editing
        
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_date = request.POST.get('event_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        status = request.POST.get('status')
        description = request.POST.get('description')
        
        organizer = request.POST.get('organizer')
        contact_person = request.POST.get('contact_person')
        contact_phone = request.POST.get('contact_phone')
        reg_start = request.POST.get('registration_start_date')
        reg_end = request.POST.get('registration_end_date')
        max_participants = request.POST.get('max_participants')
        
        venue = None
        if venue_id and venue_id != '0':
            try:
                venue = EventVenue.objects.get(venue_id=venue_id)
            except:
                pass
                
        if event_id:
            # Update existing
            event = EventMaster.objects.get(event_id=event_id)
            event.event_name = event_name
            event.event_type = event_type
            event.event_date = event_date
            event.start_time = start_time
            event.end_time = end_time
            event.venue = venue
            event.status = status
            event.description = description
            event.organizer = organizer
            event.contact_person = contact_person
            event.contact_phone = contact_phone
            event.registration_start_date = reg_start if reg_start else None
            event.registration_end_date = reg_end if reg_end else None
            event.max_participants = max_participants if max_participants else None
            event.save()
            
            from django.contrib import messages
            messages.success(request, 'Event updated successfully!')
        else:
            # Create new
            event = EventMaster.objects.create(
                event_name=event_name,
                event_type=event_type,
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                venue=venue,
                status=status,
                description=description,
                organizer=organizer,
                contact_person=contact_person,
                contact_phone=contact_phone,
                registration_start_date=reg_start if reg_start else None,
                registration_end_date=reg_end if reg_end else None,
                max_participants=max_participants if max_participants else None,
                created_by=user
            )
            
            from django.contrib import messages
            messages.success(request, 'Event added successfully!')
            
        return redirect(f'/events/?tab=details&event_id={event.event_id}')
        
    return redirect('/events/?tab=create')"""

content = re.sub(old_view, new_view, content, flags=re.DOTALL)

with open('website/views.py', 'w') as f:
    f.write(content)
