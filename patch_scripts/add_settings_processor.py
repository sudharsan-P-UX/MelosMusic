import re

with open('website/context_processors.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_proc = """import json
import os
from django.conf import settings

def security_settings(request):
    security = {'phone_length': 10, 'email_length': 255}
    try:
        path = os.path.join(settings.BASE_DIR, 'security_settings.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                security.update(data)
    except:
        pass
    return {'security_settings': security}

"""

text = new_proc + text

with open('website/context_processors.py', 'w', encoding='utf-8') as f:
    f.write(text)
