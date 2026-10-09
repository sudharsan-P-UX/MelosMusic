import re

with open('templates/website/audit_logs.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("{% extends 'website/base.html' %}", "{% extends 'base.html' %}")

with open('templates/website/audit_logs.html', 'w', encoding='utf-8') as f:
    f.write(text)
