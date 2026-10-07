with open('templates/base.html', 'r') as f:
    content = f.read()

content = content.replace("{% url 'generic_page' 'pending-fees' %}", "{% url 'pending_fees' %}")
content = content.replace("{% url 'generic_page' 'receipts' %}", "{% url 'receipts' %}")
content = content.replace("{% url 'generic_page' 'refunds' %}", "{% url 'refunds' %}")

with open('templates/base.html', 'w') as f:
    f.write(content)
