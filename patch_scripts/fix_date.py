with open('templates/website/students.html', 'r') as f:
    content = f.read()

bad_string = '{{ batch.start_date|date:"H:i" }} - {{ batch.end_date|date:"H:i" }}'
good_string = '{% if batch.start_time and batch.end_time %}{{ batch.start_time|time:"g:i A" }} - {{ batch.end_time|time:"g:i A" }}{% else %}{{ batch.batch_name }}{% endif %}'

content = content.replace(bad_string, good_string)

with open('templates/website/students.html', 'w') as f:
    f.write(content)
