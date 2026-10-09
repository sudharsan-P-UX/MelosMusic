import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Update the redirect in courses_batches_view for add_batch
old_add_batch_return = """            messages.success(request, 'Batch added successfully!')
        return redirect('courses')"""

new_add_batch_return = """            messages.success(request, 'Batch added successfully!')
            return redirect('/courses/?tab=batches')
        return redirect('courses')"""

content = content.replace(old_add_batch_return, new_add_batch_return)

with open('website/views.py', 'w') as f:
    f.write(content)
