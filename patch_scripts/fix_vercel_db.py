import re

with open('core/settings.py', 'r') as f:
    content = f.read()

# Modify DATABASES to handle Vercel read-only filesystem if DATABASE_URL is missing
old_db = """DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}"""

new_db = """# Check if we are on Vercel and DATABASE_URL is missing
default_sqlite_path = f'sqlite:///{BASE_DIR}/db.sqlite3'
if os.environ.get('VERCEL') == '1' and not os.environ.get('DATABASE_URL'):
    default_sqlite_path = 'sqlite:////tmp/db.sqlite3'

DATABASES = {
    'default': dj_database_url.config(
        default=default_sqlite_path,
        conn_max_age=600,
        conn_health_checks=True,
    )
}"""

if 'default_sqlite_path' not in content:
    content = content.replace(old_db, new_db)

with open('core/settings.py', 'w') as f:
    f.write(content)
