import re

with open('users/models.py', 'r') as f:
    content = f.read()

old_fields = """    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')"""

new_fields = """    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    display_order = models.IntegerField(default=0, db_column='DisplayOrder')"""

content = content.replace(old_fields, new_fields)

with open('users/models.py', 'w') as f:
    f.write(content)
