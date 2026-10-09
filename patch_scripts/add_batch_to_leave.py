import re

with open('academics/models.py', 'r') as f:
    content = f.read()

old_leave_model = "    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')"

new_leave_model = """    batch = models.ForeignKey('Batch', on_delete=models.SET_NULL, null=True, blank=True, db_column='BatchId')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')"""

if "batch = models.ForeignKey('Batch'" not in content:
    content = content.replace(old_leave_model, new_leave_model)
    with open('academics/models.py', 'w') as f:
        f.write(content)
