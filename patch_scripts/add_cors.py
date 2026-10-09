import os

# Add to requirements.txt
with open('requirements.txt', 'a') as f:
    f.write('\ndjango-cors-headers>=4.3.0\n')

# Update settings.py
with open('core/settings.py', 'r', encoding='utf-8') as f:
    settings = f.read()

if 'corsheaders' not in settings:
    settings = settings.replace(
        "INSTALLED_APPS = [",
        "INSTALLED_APPS = [\n    'corsheaders',"
    )
    settings = settings.replace(
        "MIDDLEWARE = [",
        "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
    )
    settings += "\n# CORS Config for Mobile App Testing in Web Emulators\nCORS_ALLOW_ALL_ORIGINS = True\n"

with open('core/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings)
