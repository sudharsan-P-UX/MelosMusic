import re

with open('templates/base.html', 'r') as f:
    content = f.read()

# Extract the existing nav block
nav_match = re.search(r'<nav id="sidebar-nav" class="flex-1 overflow-y-auto py-4 px-3 space-y-1">.*?</nav>', content, re.DOTALL)
if nav_match:
    old_nav = nav_match.group(0)
    
    new_nav = """<nav id="sidebar-nav" class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
            {% for menu in sidebar_menus %}
                {% if menu.children %}
                <div x-data="{ open: false }" x-init="const paths = [{% for c in menu.children %}'{{ c.url_page }}'{% if not forloop.last %},{% endif %}{% endfor %}]; if(paths.some(p => window.location.pathname.includes(p.split('?')[0]) && p.split('?')[0] !== '/')) open = true;">
                    <button @click="open = !open" class="w-full flex justify-between items-center px-4 py-2 text-sm rounded-md hover:bg-indigo-700 focus:outline-none">
                        <span>{{ menu.menu_name }}</span>
                        <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200" :class="{'rotate-180': open}"></i>
                    </button>
                    <div x-show="open" class="pl-4 mt-1 space-y-1">
                        {% for child in menu.children %}
                        <a href="{{ child.url_page }}" class="block px-4 py-1.5 rounded-md text-xs {% if request.get_full_path == child.url_page or request.path == child.url_page %}bg-indigo-600 text-white font-medium{% else %}text-indigo-200 hover:text-white hover:bg-indigo-700/50{% endif %} transition-colors">{{ child.menu_name }}</a>
                        {% endfor %}
                    </div>
                </div>
                {% else %}
                <a href="{{ menu.url_page }}" class="block px-4 py-2 text-sm rounded-md {% if request.get_full_path == menu.url_page or request.path == menu.url_page %}bg-indigo-600 text-white font-medium{% else %}hover:bg-indigo-700{% endif %}">{{ menu.menu_name }}</a>
                {% endif %}
            {% endfor %}
        </nav>"""
        
    content = content.replace(old_nav, new_nav)
    
    with open('templates/base.html', 'w') as f:
        f.write(content)
    print("Sidebar updated to be dynamic.")
else:
    print("Could not find nav block.")
