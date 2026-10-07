with open('academics/models.py', 'r') as f:
    content = f.read()

if 'room_number =' not in content:
    content = content.replace("end_time = models.TimeField(db_column='EndTime')", "end_time = models.TimeField(db_column='EndTime')\n    room_number = models.CharField(max_length=255, null=True, blank=True, db_column='RoomNumber')")

new_attendance = '''class AttendanceRecord(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')])
    remarks = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attendance_records'
'''
if 'AttendanceRecord' not in content:
    content += '\n' + new_attendance

if 'description =' not in content:
    content = content.replace("course_name = models.CharField(max_length=255, db_column='CourseName')", "course_name = models.CharField(max_length=255, db_column='CourseName')\n    description = models.TextField(null=True, blank=True, db_column='Description')\n    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='FeeAmount')")

with open('academics/models.py', 'w') as f:
    f.write(content)
