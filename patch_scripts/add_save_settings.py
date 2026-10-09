import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = "        if action == 'create_user' and not admin_access.add_access:"

good = """        if action == 'save_settings':
            import json, os
            from django.conf import settings
            
            phone_length = request.POST.get('phone_length', 10)
            email_length = request.POST.get('email_length', 255)
            password_expire = request.POST.get('password_expire', 90)
            
            data = {
                'phone_length': int(phone_length),
                'email_length': int(email_length),
                'password_expire': int(password_expire)
            }
            path = os.path.join(settings.BASE_DIR, 'security_settings.json')
            with open(path, 'w') as fh:
                json.dump(data, fh)
            
            messages.success(request, 'Settings saved successfully.')
            return redirect('/admin-dashboard/?tab=settings')
            
        if action == 'create_user' and not admin_access.add_access:"""

text = text.replace(bad, good)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
