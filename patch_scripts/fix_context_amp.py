import re

with open('website/context_processors.py', 'r') as f:
    content = f.read()

content = content.replace(
    "perms[access.menu.menu_name.replace(' ', '_')] = {",
    "perms[access.menu.menu_name.replace(' & ', '_and_').replace(' ', '_')] = {"
)

with open('website/context_processors.py', 'w') as f:
    f.write(content)
