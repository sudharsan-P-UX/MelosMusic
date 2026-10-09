with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = "    }.replace('}', '    \\'allocated_batches\\': allocated_batches\n    }'))"
good = ",\n        'allocated_batches': allocated_batches\n    })"

text = text.replace(bad, good)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
