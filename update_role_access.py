import re

with open('users/models.py', 'r') as f:
    content = f.read()

# Add export_access and approve_access to RoleAccess
if 'export_access' not in content:
    old_role_access = """    delete_access = models.BooleanField(default=False, db_column='DeleteAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')"""
    new_role_access = """    delete_access = models.BooleanField(default=False, db_column='DeleteAccess')
    export_access = models.BooleanField(default=False, db_column='ExportAccess')
    approve_access = models.BooleanField(default=False, db_column='ApproveAccess')
    is_active = models.BooleanField(default=True, db_column='IsActive')"""
    content = content.replace(old_role_access, new_role_access)

with open('users/models.py', 'w') as f:
    f.write(content)
