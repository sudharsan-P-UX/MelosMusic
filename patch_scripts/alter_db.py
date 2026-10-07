import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
cursor = connection.cursor()

try:
    cursor.execute('ALTER TABLE "MasterMenu" ADD COLUMN "ApproveAccess" boolean DEFAULT false;')
except Exception as e:
    print(e)
    connection.rollback()
    
try:
    cursor.execute('ALTER TABLE "MasterMenu" ADD COLUMN "ExportAccess" boolean DEFAULT false;')
except Exception as e:
    print(e)
    connection.rollback()

connection.commit()
print("Done")
