import os
import re

def fix_course_creation():
    with open('website/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r"duration_months=request\.POST\.get\('duration_months'\),",
        r"duration_months=request.POST.get('duration_months') or None,",
        content
    )
    content = re.sub(
        r"total_sessions=request\.POST\.get\('total_sessions'\),",
        r"total_sessions=request.POST.get('total_sessions') or None,",
        content
    )
    content = re.sub(
        r"fee_amount=request\.POST\.get\('fee_amount'\),",
        r"fee_amount=request.POST.get('fee_amount') or 0.00,",
        content
    )
    content = re.sub(
        r"days=request\.POST\.get\('days'\),",
        r"days=request.POST.get('days') or None,",
        content
    )

    with open('website/views.py', 'w', encoding='utf-8') as f:
        f.write(content)

fix_course_creation()
print("Fixed views.py empty string conversion for Course fields.")
