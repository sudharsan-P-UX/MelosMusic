import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make the AlpineJS auto-expand logic more robust by stripping trailing slashes for comparison
old_js = "if(paths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;"
new_js = "if(paths.some(p => { const path = p.split('?')[0].replace(/\\/$/, ''); return window.location.pathname.replace(/\\/$/, '').includes(path) && path !== ''; })) open = true;"

text = text.replace(old_js, new_js)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(text)
