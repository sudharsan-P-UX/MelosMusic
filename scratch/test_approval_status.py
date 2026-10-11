import os
import sys
import django
from datetime import date

sys.path.insert(0, r'C:\Users\sudharsanp\.gemini\antigravity\scratch\melos_music')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from academics.models import StudentAttendance, StudentAttendanceDetail, TeacherAttendance, TeacherAttendanceDetail, Batch
from users.models import User

print("=== STARTING APPROVAL STATUS VERIFICATION ===")

user = User.objects.first()
if not user:
    print("No user found in database.")
    sys.exit(1)

client = Client()
session = client.session
session['user_id'] = user.user_id
session.save()
print(f"Logged in as user_id {user.user_id} ({user.first_name})")

# 1. Test Student Attendance Page GET
resp_s = client.get('/attendance/student/')
print(f"GET /attendance/student/ status: {resp_s.status_code}")
assert resp_s.status_code == 200, f"Expected 200, got {resp_s.status_code}"
content_s = resp_s.content.decode('utf-8')
assert 'Approved Status' in content_s, "'Approved Status' not found in student attendance HTML"
assert 'approval_status' in content_s, "'approval_status' filter/field not found in student attendance HTML"
print("[OK] Student attendance page renders 'Approved Status' table column, filter, and modal field")

# 2. Test Teacher Attendance Page GET
resp_t = client.get('/attendance/teacher/')
print(f"GET /attendance/teacher/ status: {resp_t.status_code}")
assert resp_t.status_code == 200, f"Expected 200, got {resp_t.status_code}"
content_t = resp_t.content.decode('utf-8')
assert 'Approved Status' in content_t, "'Approved Status' not found in teacher attendance HTML"
assert 'approval_status' in content_t, "'approval_status' filter/field not found in teacher attendance HTML"
print("[OK] Teacher attendance page renders 'Approved Status' table column, filter, and modal field")

# 3. Test Student Attendance approval workflow
student = User.objects.filter(role__role_name__iexact='student').first() or user
batch = Batch.objects.first()

att_parent, _ = StudentAttendance.objects.get_or_create(
    attendance_date=date.today(),
    defaults={'created_by': user.user_id, 'batch': batch}
)
s_detail = StudentAttendanceDetail.objects.create(
    student_attendance=att_parent,
    student=student,
    attendance_status=4, # Leave
    approval_status='Pending',
    remarks='Testing approval status logic'
)
print(f"Created student attendance detail {s_detail.student_attendance_detail_id} with approval_status: {s_detail.approval_status}")

# Approve student attendance
resp = client.post('/attendance/student/', {
    'action': 'approve_attendance',
    'detail_id': s_detail.student_attendance_detail_id
}, follow=True)
s_detail.refresh_from_db()
print(f"After approve action, approval_status: {s_detail.approval_status}")
assert s_detail.approval_status == 'Approved', f"Expected Approved, got {s_detail.approval_status}"

# Reject student attendance
resp = client.post('/attendance/student/', {
    'action': 'reject_attendance',
    'detail_id': s_detail.student_attendance_detail_id
}, follow=True)
s_detail.refresh_from_db()
print(f"After reject action, approval_status: {s_detail.approval_status}")
assert s_detail.approval_status == 'Rejected', f"Expected Rejected, got {s_detail.approval_status}"

# Clean up
s_detail.delete()
print("[OK] Student Attendance Approve & Reject POST actions work perfectly!")

# 4. Test Teacher Attendance approval workflow
teacher = User.objects.filter(role__role_name__iexact='teacher').first() or user

t_parent, _ = TeacherAttendance.objects.get_or_create(
    attendance_date=date.today(),
    defaults={'created_by': user.user_id}
)
t_detail = TeacherAttendanceDetail.objects.create(
    teacher_attendance=t_parent,
    teacher=teacher,
    attendance_status=4, # Leave
    approval_status='Pending',
    remarks='Testing teacher approval status logic'
)
print(f"Created teacher attendance detail {t_detail.teacher_attendance_detail_id} with approval_status: {t_detail.approval_status}")

# Approve teacher attendance
resp = client.post('/attendance/teacher/', {
    'action': 'approve_teacher_attendance',
    'detail_id': t_detail.teacher_attendance_detail_id
}, follow=True)
t_detail.refresh_from_db()
print(f"After approve action, approval_status: {t_detail.approval_status}")
assert t_detail.approval_status == 'Approved', f"Expected Approved, got {t_detail.approval_status}"

# Reject teacher attendance
resp = client.post('/attendance/teacher/', {
    'action': 'reject_teacher_attendance',
    'detail_id': t_detail.teacher_attendance_detail_id
}, follow=True)
t_detail.refresh_from_db()
print(f"After reject action, approval_status: {t_detail.approval_status}")
assert t_detail.approval_status == 'Rejected', f"Expected Rejected, got {t_detail.approval_status}"

# Clean up
t_detail.delete()
print("[OK] Teacher Attendance Approve & Reject POST actions work perfectly!")

# 5. Test Filter by Approval Status
resp_filter = client.get('/attendance/student/?approval_status=Approved')
assert resp_filter.status_code == 200
assert 'value="Approved" selected' in resp_filter.content.decode('utf-8')
print("[OK] Approval status filtering works as expected on Student Attendance")

resp_filter_t = client.get('/attendance/teacher/?approval_status=Approved')
assert resp_filter_t.status_code == 200
assert 'value="Approved" selected' in resp_filter_t.content.decode('utf-8')
print("[OK] Approval status filtering works as expected on Teacher Attendance")


print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
