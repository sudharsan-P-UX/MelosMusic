with open('templates/base.html', 'r') as f:
    content = f.read()

content = content.replace("{% url 'generic_page' 'courses' %}", "{% url 'courses' %}")

with open('templates/base.html', 'w') as f:
    f.write(content)
