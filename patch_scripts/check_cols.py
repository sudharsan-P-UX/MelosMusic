import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT * FROM "MasterMenu" LIMIT 1')
for col in cursor.description:
    print(col[0])
