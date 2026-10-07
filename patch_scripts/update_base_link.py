with open('templates/base.html', 'r') as f:
    content = f.read()

content = content.replace("{% url 'page' 'timetable' %}", "{% url 'timetable' %}")

with open('templates/base.html', 'w') as f:
    f.write(content)
