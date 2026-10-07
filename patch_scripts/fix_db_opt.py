import re

with open('website/views.py', 'r') as f:
    content = f.read()

old_block = """                # Update conflicts (Django 4.1+) natively translates this to a single UPSERT query
                RoleAccess.objects.bulk_create(
                    role_access_instances,
                    update_conflicts=True,
                    unique_fields=['role', 'menu'],
                    update_fields=['view_access', 'add_access', 'edit_access', 'delete_access', 'export_access', 'created_by']
                )"""

new_block = """                # Optimized Bulk Operation to eliminate N+1 network latency
                # Delete existing permissions for this role (1 query)
                RoleAccess.objects.filter(role=role).delete()
                # Bulk insert all new permissions (1 query)
                RoleAccess.objects.bulk_create(role_access_instances)"""

content = content.replace(old_block, new_block)

with open('website/views.py', 'w') as f:
    f.write(content)
