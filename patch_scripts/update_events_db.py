with open('events/models.py', 'r') as f:
    content = f.read()

# Add target_batch_id to Event
if 'target_batch' not in content:
    # Need to import Batch
    if 'from academics.models import Batch' not in content:
        content = content.replace('from users.models import Role', 'from users.models import Role, User\nfrom academics.models import Batch')
    content = content.replace("venue = models.CharField(max_length=500, db_column='Venue')", "venue = models.CharField(max_length=500, db_column='Venue')\n    target_batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, db_column='TargetBatchId')")

# Update Notification to link to User
if 'user =' not in content:
    content = content.replace("role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='RoleId')", "user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId', null=True)")

with open('events/models.py', 'w') as f:
    f.write(content)
