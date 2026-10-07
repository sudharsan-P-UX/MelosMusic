import re

with open('website/views.py', 'r') as f:
    content = f.read()

# Add messages import
if 'from django.contrib import messages' not in content:
    content = content.replace('from django.shortcuts import render, redirect', 'from django.shortcuts import render, redirect\nfrom django.contrib import messages')

# Inject in login
content = content.replace("request.session['user_id'] = user.user_id\n                return redirect('dashboard')", "request.session['user_id'] = user.user_id\n                messages.success(request, f'Welcome back, {user.display_name}!')\n                return redirect('dashboard')")
content = content.replace("error_msg = 'Invalid username or password'", "messages.error(request, 'Invalid username or password')\n            error_msg = 'Invalid username or password'")

# Inject in logout
content = content.replace("request.session.flush()\n    return redirect('login')", "request.session.flush()\n    messages.success(request, 'You have been logged out.')\n    return redirect('login')")

# Inject in students creation
content = content.replace("UserCourse.objects.create(user=new_student, course=course)\n            \n        return redirect('students')", "UserCourse.objects.create(user=new_student, course=course)\n            \n        messages.success(request, 'Student added successfully!')\n        return redirect('students')")

# Inject in students update
content = content.replace("student.save()\n            \n            return redirect('students')", "student.save()\n            \n            messages.success(request, 'Student updated successfully!')\n            return redirect('students')")

# Inject in student delete
content = content.replace("student.delete()\n        return redirect('students')", "student.delete()\n        messages.success(request, 'Student deleted successfully!')\n        return redirect('students')")

# Inject in teachers creation
content = content.replace("UserCourse.objects.create(user=new_teacher, course=course)\n            \n        return redirect('teachers')", "UserCourse.objects.create(user=new_teacher, course=course)\n            \n        messages.success(request, 'Teacher added successfully!')\n        return redirect('teachers')")

# Inject in teachers update
content = content.replace("teacher.save()\n            \n            return redirect('teachers')", "teacher.save()\n            \n            messages.success(request, 'Teacher updated successfully!')\n            return redirect('teachers')")

# Inject in teacher delete
content = content.replace("teacher.delete()\n        return redirect('teachers')", "teacher.delete()\n        messages.success(request, 'Teacher deleted successfully!')\n        return redirect('teachers')")

with open('website/views.py', 'w') as f:
    f.write(content)
