import re

with open('core/settings.py', 'r', encoding='utf-8') as f:
    settings = f.read()

# Disable XFrameOptionsMiddleware for webview embedding in FlutLab
settings = settings.replace(
    "'django.middleware.clickjacking.XFrameOptionsMiddleware',",
    "# 'django.middleware.clickjacking.XFrameOptionsMiddleware',"
)

with open('core/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings)
