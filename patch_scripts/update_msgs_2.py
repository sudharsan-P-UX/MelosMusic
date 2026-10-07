with open('website/views.py', 'r') as f:
    content = f.read()

# Fix Teacher Update
content = content.replace("except User.DoesNotExist:\n            pass\n            \n    return redirect('teachers')", "except User.DoesNotExist:\n            pass\n            \n    messages.success(request, 'Teacher updated successfully!')\n    return redirect('teachers')")

# Fix Teacher Delete
content = content.replace("except User.DoesNotExist:\n        pass\n    return redirect('teachers')", "except User.DoesNotExist:\n        pass\n    messages.success(request, 'Teacher deleted successfully!')\n    return redirect('teachers')")

with open('website/views.py', 'w') as f:
    f.write(content)
