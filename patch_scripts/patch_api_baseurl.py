import re

with open('mobile_app/lib/api_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "static const String baseUrl = 'http://10.0.2.2:8000/api';",
    "static const String baseUrl = 'https://melosmusic.vercel.app/api';"
)

with open('mobile_app/lib/api_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)
