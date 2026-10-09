import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update student_attendance_view to fetch allocated batches
student_view_pattern = r"(def student_attendance_view\(request\):.*?)(    selected_batch = request\.GET\.get\('batch_id', ''\))"

new_student_view_insert = """    from academics.models import StudentEnrollment
    allocated_batches = [e.batch for e in StudentEnrollment.objects.filter(student=user, status=1, batch__isnull=False).select_related('batch')]
    
"""

content = re.sub(student_view_pattern, r'\1' + new_student_view_insert + r'\2', content, flags=re.DOTALL)

# Add allocated_batches to context in student_attendance_view
student_context_pattern = r"('selected_date': selected_date\n    \})"
content = re.sub(student_context_pattern, r"\1.replace('}', '    \\'allocated_batches\\': allocated_batches\n    }')", content, flags=re.DOTALL) # wait, string replacement is tricky with regex. Let's do it manually

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Use python replacement for context since regex with dicts is annoying
with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace("'selected_date': selected_date\n    })", "'selected_date': selected_date,\n        'allocated_batches': allocated_batches\n    })")
with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)

# Update teacher_attendance_view to fetch allocated batches
teacher_view_pattern = r"(def teacher_attendance_view\(request\):.*?)(    selected_teacher = request\.GET\.get\('teacher_id', ''\))"

new_teacher_view_insert = """    from academics.models import Batch
    allocated_batches = list(Batch.objects.filter(teacher=user, is_active=True))
    
"""
with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(teacher_view_pattern, r'\1' + new_teacher_view_insert + r'\2', text, flags=re.DOTALL)

# Add allocated_batches to context in teacher_attendance_view
text = text.replace("'selected_date': selected_date\n    })", "'selected_date': selected_date,\n        'allocated_batches': allocated_batches\n    })")

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("views.py updated")
