import re

with open('website/views.py', 'r') as f:
    content = f.read()

# student
old_s = """                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days'),
                request_type=request.POST.get('request_type'),"""

new_s = """                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),"""
content = content.replace(old_s, new_s)

# teacher
old_t = """                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days'),
                request_type=request.POST.get('request_type'),"""
                
new_t = """                from_date=request.POST.get('from_date'),
                to_date=request.POST.get('to_date'),
                no_of_days=request.POST.get('no_of_days') or 1,
                request_type=request.POST.get('request_type'),"""

# wait, since I did a replace and they are identical strings, the first replace might have replaced both if they were identical!
# actually, let's just use string replace on the exact text.

with open('website/views.py', 'r') as f:
    original = f.read()
    
updated = original.replace("no_of_days=request.POST.get('no_of_days'),", "no_of_days=request.POST.get('no_of_days') or 1,")

with open('website/views.py', 'w') as f:
    f.write(updated)
