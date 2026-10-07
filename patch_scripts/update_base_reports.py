with open('templates/base.html', 'r') as f:
    content = f.read()

content = content.replace("{% url 'generic_page' 'reports' %}", "{% url 'reports' %}")

with open('templates/base.html', 'w') as f:
    f.write(content)
