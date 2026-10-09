import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Update add_course
old_add_course = """        if action == 'add_course':
            Course.objects.create(
                course_code=request.POST.get('course_code'),"""

new_add_course = """        if action == 'add_course':
            course_code = request.POST.get('course_code')
            if not course_code:
                last_course = Course.objects.exclude(course_code__isnull=True).exclude(course_code='').order_by('-course_id').first()
                if last_course and last_course.course_code.startswith('C'):
                    try:
                        num = int(last_course.course_code[1:]) + 1
                        course_code = f"C{num}"
                    except:
                        course_code = "C1000"
                else:
                    course_code = "C1000"
            
            Course.objects.create(
                course_code=course_code,"""

content = content.replace(old_add_course, new_add_course)


# Update add_batch
old_add_batch = """        elif action == 'add_batch':
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            Batch.objects.create(
                batch_code=request.POST.get('batch_code'),"""

new_add_batch = """        elif action == 'add_batch':
            batch_code = request.POST.get('batch_code')
            if not batch_code:
                last_batch = Batch.objects.exclude(batch_code__isnull=True).exclude(batch_code='').order_by('-batch_id').first()
                if last_batch and last_batch.batch_code.startswith('B'):
                    try:
                        num = int(last_batch.batch_code[1:]) + 1
                        batch_code = f"B{num}"
                    except:
                        batch_code = "B1000"
                else:
                    batch_code = "B1000"
                    
            course_id = request.POST.get('course_id')
            teacher_id = request.POST.get('teacher_id')
            Batch.objects.create(
                batch_code=batch_code,"""

content = content.replace(old_add_batch, new_add_batch)

with open('website/views.py', 'w') as f:
    f.write(content)
