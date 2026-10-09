import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Replace the enrollments query to select_related exactly like in allocation
old_query = "enrollments = StudentEnrollment.objects.all().order_by('-created_date')"
new_query = "enrollments = StudentEnrollment.objects.select_related('student', 'course', 'batch', 'batch__teacher').exclude(batch__isnull=True).order_by('-created_date')"

content = content.replace(old_query, new_query)

# Also update the page_title in the context to 'Allocation Details'
content = content.replace("'page_title': 'Student Course',", "'page_title': 'Allocation Details',")

with open('website/views.py', 'w') as f:
    f.write(content)
