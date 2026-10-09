import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Replace the array syntax with string split syntax for both parent and child
old_parent_init = """x-init="const paths = [{% for c in menu.children %}'{{ c.url_page }}'{% if not forloop.last %},{% endif %}{% for cc in c.children %},'{{ cc.url_page }}'{% endfor %}{% endfor %}]; if(paths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;\""""
new_parent_init = """x-init="const paths = `{% for c in menu.children %}{{ c.url_page }}|{% for cc in c.children %}{{ cc.url_page }}|{% endfor %}{% endfor %}`.split('|').filter(Boolean); if(paths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;\""""

old_child_init = """x-init="const childPaths = [{% for cc in child.children %}'{{ cc.url_page }}'{% if not forloop.last %},{% endif %}{% endfor %}]; if(childPaths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;\""""
new_child_init = """x-init="const childPaths = `{% for cc in child.children %}{{ cc.url_page }}|{% endfor %}`.split('|').filter(Boolean); if(childPaths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;\""""

content = content.replace(old_parent_init, new_parent_init)
content = content.replace(old_child_init, new_child_init)

with open('templates/base.html', 'w') as f:
    f.write(content)
