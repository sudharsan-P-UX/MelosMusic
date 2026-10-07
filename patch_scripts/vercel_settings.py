import re

with open('core/settings.py', 'r') as f:
    content = f.read()

# 1. Add dj_database_url import and change DATABASES
if 'import dj_database_url' not in content:
    content = 'import dj_database_url\nimport os\n' + content

old_databases = r"DATABASES = \{\s*'default': \{\s*'ENGINE': 'django\.db\.backends\.sqlite3',\s*'NAME': BASE_DIR / 'db\.sqlite3',\s*\}\s*\}"
new_databases = """DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}"""
content = re.sub(old_databases, new_databases, content, flags=re.DOTALL)


# 2. Add Whitenoise middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in content:
    old_middleware = r"MIDDLEWARE = \[\s*('|\")django\.middleware\.security\.SecurityMiddleware('|\"),"
    new_middleware = "MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
    content = re.sub(old_middleware, new_middleware, content)

# 3. Static files config for Whitenoise
if 'STATIC_ROOT' not in content:
    static_config = """

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
"""
    content += static_config

# 4. ALLOWED_HOSTS for Vercel
if "ALLOWED_HOSTS = []" in content:
    content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*'] # Allowed for all in Vercel")

with open('core/settings.py', 'w') as f:
    f.write(content)
