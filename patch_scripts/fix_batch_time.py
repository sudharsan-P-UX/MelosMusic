import os
import re

def fix_batch_creation():
    with open('website/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where Batch is created
    # We want to replace:
    # start_time=request.POST.get('start_time'),
    # with:
    # start_time=request.POST.get('start_time') or None,
    # And same for end_time, start_date, end_date.

    old_create = """Batch.objects.create(
                batch_code=batch_code,
                batch_name=request.POST.get('batch_name'),
                course_id=course_id,
                teacher_id=teacher_id if teacher_id else None,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                capacity=request.POST.get('capacity'),
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )"""

    new_create = """Batch.objects.create(
                batch_code=batch_code,
                batch_name=request.POST.get('batch_name'),
                course_id=course_id,
                teacher_id=teacher_id if teacher_id else None,
                start_date=request.POST.get('start_date') or None,
                end_date=request.POST.get('end_date') or None,
                start_time=request.POST.get('start_time') or None,
                end_time=request.POST.get('end_time') or None,
                capacity=request.POST.get('capacity') or None,
                is_active=request.POST.get('status') == 'active',
                created_by=user.user_id
            )"""

    if old_create in content:
        content = content.replace(old_create, new_create)
    else:
        # If whitespace is different, try regex
        content = re.sub(
            r"start_time=request\.POST\.get\('start_time'\),",
            r"start_time=request.POST.get('start_time') or None,",
            content
        )
        content = re.sub(
            r"end_time=request\.POST\.get\('end_time'\),",
            r"end_time=request.POST.get('end_time') or None,",
            content
        )
        content = re.sub(
            r"start_date=request\.POST\.get\('start_date'\),",
            r"start_date=request.POST.get('start_date') or None,",
            content
        )
        content = re.sub(
            r"end_date=request\.POST\.get\('end_date'\),",
            r"end_date=request.POST.get('end_date') or None,",
            content
        )
        content = re.sub(
            r"capacity=request\.POST\.get\('capacity'\),",
            r"capacity=request.POST.get('capacity') or None,",
            content
        )

    with open('website/views.py', 'w', encoding='utf-8') as f:
        f.write(content)

fix_batch_creation()
print("Fixed views.py empty string conversion for Time/Date fields.")
