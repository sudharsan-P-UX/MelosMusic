import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Replace the simple query with filtered query
old_query = "events = EventMaster.objects.all().order_by('-event_date')"
new_query = """events = EventMaster.objects.all().order_by('-event_date')
    
    search = request.GET.get('search')
    if search:
        events = events.filter(event_name__icontains=search)
        
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
        
    status = request.GET.get('status')
    if status:
        events = events.filter(status=status)
        
    from_date = request.GET.get('from_date')
    if from_date:
        events = events.filter(event_date__gte=from_date)
        
    to_date = request.GET.get('to_date')
    if to_date:
        events = events.filter(event_date__lte=to_date)"""

content = content.replace(old_query, new_query)

with open('website/views.py', 'w') as f:
    f.write(content)
