with open('academics/models.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r"\'", "'")

with open('academics/models.py', 'w', encoding='utf-8') as f:
    f.write(text)
