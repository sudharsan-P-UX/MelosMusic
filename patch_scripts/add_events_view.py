with open('website/views.py', 'r') as f:
    content = f.read()

new_view = """def events_dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    user = User.objects.get(user_id=request.session['user_id'])
    
    from events.models import EventMaster, EventParticipant, EventVenue, EventAttendance
    
    events = EventMaster.objects.all().order_by('-event_date')
    venues = EventVenue.objects.all()
    participants = EventParticipant.objects.all()
    attendance = EventAttendance.objects.all()
    
    tab = request.GET.get('tab', 'calendar')
    
    return render(request, 'website/events_dashboard.html', {
        'user': user,
        'page_title': 'Event Scheduling',
        'events': events,
        'venues': venues,
        'participants': participants,
        'attendance': attendance,
        'active_tab': tab
    })

def generic_page"""

content = content.replace('def generic_page', new_view)

with open('website/views.py', 'w') as f:
    f.write(content)
