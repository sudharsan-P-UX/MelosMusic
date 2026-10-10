import os
import re

def patch_views():
    with open('website/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add duration_hrs to Course.objects.create in add_course
    if 'duration_hrs=request.POST.get' not in content:
        content = re.sub(
            r"duration_months=request\.POST\.get\('duration_months'\) or None,",
            r"duration_months=request.POST.get('duration_months') or None,\n                duration_hrs=request.POST.get('duration_hrs') or None,",
            content
        )

    with open('website/views.py', 'w', encoding='utf-8') as f:
        f.write(content)

patch_views()
print("Patched views.py for course duration_hrs.")
