import re

with open('academics/models.py', 'r') as f:
    content = f.read()

# Replace AttendanceRecord block completely
content = re.sub(r"class AttendanceRecord.*?db_table = 'attendance_records'", "", content, flags=re.DOTALL)

new_models = """
class StudentAttendance(models.Model):
    student_attendance_id = models.AutoField(primary_key=True, db_column='StudentAttendanceId')
    attendance_date = models.DateField(db_column='AttendanceDate')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseId', null=True, blank=True)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, db_column='BatchId', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    last_changed_date = models.DateTimeField(auto_now=True, db_column='LastChangedDate', null=True)
    last_changed_by = models.IntegerField(null=True, blank=True, db_column='LastChangedBy')

    class Meta:
        db_table = 'StudentAttendance'

class StudentAttendanceDetail(models.Model):
    student_attendance_detail_id = models.AutoField(primary_key=True, db_column='StudentAttendanceDetailId')
    student_attendance = models.ForeignKey(StudentAttendance, on_delete=models.CASCADE, db_column='StudentAttendanceId')
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_column='StudentId')
    attendance_status = models.SmallIntegerField(db_column='AttendanceStatus') # 1=Present, 2=Absent, etc.
    check_in_time = models.TimeField(null=True, blank=True, db_column='CheckInTime')
    check_out_time = models.TimeField(null=True, blank=True, db_column='CheckOutTime')
    remarks = models.CharField(max_length=500, null=True, blank=True, db_column='Remarks')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'StudentAttendanceDetail'

class TeacherAttendance(models.Model):
    teacher_attendance_id = models.AutoField(primary_key=True, db_column='TeacherAttendanceId')
    attendance_date = models.DateField(db_column='AttendanceDate')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'TeacherAttendance'

class TeacherAttendanceDetail(models.Model):
    teacher_attendance_detail_id = models.AutoField(primary_key=True, db_column='TeacherAttendanceDetailId')
    teacher_attendance = models.ForeignKey(TeacherAttendance, on_delete=models.CASCADE, db_column='TeacherAttendanceId')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, db_column='TeacherId')
    attendance_status = models.SmallIntegerField(db_column='AttendanceStatus')
    check_in_time = models.TimeField(null=True, blank=True, db_column='CheckInTime')
    check_out_time = models.TimeField(null=True, blank=True, db_column='CheckOutTime')
    remarks = models.CharField(max_length=500, null=True, blank=True, db_column='Remarks')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'TeacherAttendanceDetail'
"""

if 'StudentAttendanceDetail' not in content:
    content += '\n' + new_models

with open('academics/models.py', 'w') as f:
    f.write(content)
