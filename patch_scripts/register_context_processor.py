import re

with open('core/settings.py', 'r') as f:
    content = f.read()

if "'website.context_processors.user_permissions'" not in content:
    content = content.replace(
        "'django.contrib.messages.context_processors.messages',",
        "'django.contrib.messages.context_processors.messages',\n                'website.context_processors.user_permissions',"
    )

with open('core/settings.py', 'w') as f:
    f.write(content)
