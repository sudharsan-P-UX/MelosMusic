import re

with open('core/settings.py', 'r') as f:
    content = f.read()

old_cp = """                'django.contrib.messages.context_processors.messages',
                'website.context_processors.user_permissions',"""
new_cp = """                'django.contrib.messages.context_processors.messages',
                'website.context_processors.user_permissions',
                'website.context_processors.sidebar_menu_processor',"""

content = content.replace(old_cp, new_cp)

with open('core/settings.py', 'w') as f:
    f.write(content)
