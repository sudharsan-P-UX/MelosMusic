import re

with open('academics/models.py', 'r') as f:
    content = f.read()

new_model = """
class LeaveRequest(models.Model):
    leave_request_id = models.AutoField(primary_key=True, db_column='LeaveRequestId')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, db_column='UserId')
    user_type = models.CharField(max_length=50, db_column='UserType')
    from_date = models.DateField(db_column='FromDate')
    to_date = models.DateField(db_column='ToDate')
    no_of_days = models.IntegerField(db_column='NoOfDays')
    request_type = models.CharField(max_length=100, db_column='RequestType')
    applied_date = models.DateTimeField(auto_now_add=True, db_column='AppliedDate')
    manager_approval_on = models.DateTimeField(null=True, blank=True, db_column='ManagerApprovalOn')
    manager_approval_status = models.CharField(max_length=50, default='Pending', db_column='ManagerApprovalStatus')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'LeaveRequest'
"""

content += new_model

with open('academics/models.py', 'w') as f:
    f.write(content)
