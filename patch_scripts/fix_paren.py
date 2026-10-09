with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad_string = "        'allocated_batches': allocated_batches\n    }"
good_string = "        'allocated_batches': allocated_batches\n    })"

text = text.replace(bad_string, good_string)

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
