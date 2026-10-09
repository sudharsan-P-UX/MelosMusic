with open('core/settings.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = "'website.context_processors.current_menu_access_processor',"
good = "'website.context_processors.current_menu_access_processor',\n                'website.context_processors.security_settings',"

text = text.replace(bad, good)

with open('core/settings.py', 'w', encoding='utf-8') as f:
    f.write(text)
