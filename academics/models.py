from django.db import models
from users.models import User

class Course(models.Model):
    course_id = models.AutoField(primary_key=True, db_column='CourseId')
    course_code = models.CharField(max_length=50, null=True, blank=True, db_column='CourseCode')
    course_name = models.CharField(max_length=255, db_column='CourseName')
    category = models.CharField(max_length=100, null=True, blank=True, db_column='Category')
    duration_months = models.IntegerField(null=True, blank=True, db_column='DurationMonths')
    duration_hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='DurationHrs')
    total_sessions = models.IntegerField(null=True, blank=True, db_column='TotalSessions')
    days = models.CharField(max_length=200, null=True, blank=True, db_column='Days')
    description = models.TextField(null=True, blank=True, db_column='Description')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='FeeAmount')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'Course'



class UserCourse(models.Model):
    user_course_id = models.AutoField(primary_key=True, db_column='UserCourseId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseId')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    last_date = models.DateTimeField(auto_now=True, db_column='LastDate')
    last_changed_by = models.IntegerField(null=True, blank=True, db_column='LastChangedBy')

    class Meta:
        db_table = 'UserCourse'

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True, db_column='AttendanceId')
    attendance_name = models.CharField(max_length=100, db_column='AttendanceName')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    last_date = models.DateTimeField(auto_now=True, db_column='LastDate')
    last_changed_by = models.IntegerField(null=True, blank=True, db_column='LastChangedBy')

    class Meta:
        db_table = 'Attendance'

class UserAttendance(models.Model):
    user_attendance_id = models.AutoField(primary_key=True, db_column='UserAttendanceId')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserId')
    attendance_date = models.DateField(db_column='AttendanceDate')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, db_column='AttendanceId')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'UserAttendance'

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True, db_column='BatchId')
    batch_code = models.CharField(max_length=50, null=True, blank=True, db_column='BatchCode')
    batch_name = models.CharField(max_length=255, db_column='BatchName')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseId')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='TeacherId')
    start_date = models.DateField(db_column='StartDate', null=True)
    end_date = models.DateField(db_column='EndDate', null=True)
    start_time = models.TimeField(db_column='StartTime', null=True, blank=True)
    end_time = models.TimeField(db_column='EndTime', null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True, db_column='Capacity')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'Batch'


class Timetable(models.Model):
    timetable_id = models.AutoField(primary_key=True, db_column='TimetableId')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, db_column='BatchId')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, db_column='TeacherId')
    day_of_week = models.CharField(max_length=50, db_column='DayOfWeek')
    start_time = models.TimeField(db_column='StartTime')
    end_time = models.TimeField(db_column='EndTime')
    room_number = models.CharField(max_length=255, null=True, blank=True, db_column='RoomNumber')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'Timetable'




class StudentEnrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True, db_column='EnrollmentId')
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_column='StudentId')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseId')
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE, db_column='BatchId', null=True, blank=True)
    joining_date = models.DateField(db_column='JoiningDate', null=True, blank=True)
    status = models.SmallIntegerField(db_column='Status', default=1)
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')

    class Meta:
        db_table = 'StudentEnrollment'

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
    batch = models.ForeignKey('Batch', on_delete=models.SET_NULL, null=True, blank=True, db_column='BatchId')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')

    class Meta:
        db_table = 'LeaveRequest'
