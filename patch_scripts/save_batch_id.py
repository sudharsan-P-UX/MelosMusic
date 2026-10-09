with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("request_type=request.POST.get('request_type'),", "request_type=request.POST.get('request_type'),\n                batch_id=request.POST.get('batch_id'),")

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
