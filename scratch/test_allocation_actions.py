import os
import sys
import django

sys.path.insert(0, r'C:\Users\sudharsanp\.gemini\antigravity\scratch\melos_music')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from academics.models import Course, Batch, StudentEnrollment
from users.models import User

print("=== STARTING ALLOCATION ACTIONS VERIFICATION ===")

user = User.objects.first()
if not user:
    print("No user found in database.")
    sys.exit(1)

client = Client()
session = client.session
session['user_id'] = user.user_id
session.save()
print(f"Logged in as user_id {user.user_id} ({user.first_name})")

# 1. Test Student Allocation GET
resp_s = client.get('/student-allocation/')
print(f"GET /student-allocation/ status: {resp_s.status_code}")
assert resp_s.status_code == 200, f"Expected 200, got {resp_s.status_code}"
content_s = resp_s.content.decode('utf-8')
assert 'Actions' in content_s, "'Actions' column not found in student_allocation"
assert 'fa-eye' in content_s, "'fa-eye' view icon not found in student_allocation"
assert 'fa-pen-to-square' in content_s, "'fa-pen-to-square' edit icon not found in student_allocation"
assert 'fa-trash-can' in content_s, "'fa-trash-can' delete icon not found in student_allocation"
assert 'showViewModal' in content_s, "View modal not found in student_allocation"
assert 'showEditModal' in content_s, "Edit modal not found in student_allocation"
assert 'showDeleteModal' in content_s, "Delete modal not found in student_allocation"
print("[OK] Student Course Allocation page renders Actions column with View, Edit, Delete modals and icons")

# 2. Test Teacher Allocation GET
resp_t = client.get('/teacher-allocation/')
print(f"GET /teacher-allocation/ status: {resp_t.status_code}")
assert resp_t.status_code == 200, f"Expected 200, got {resp_t.status_code}"
content_t = resp_t.content.decode('utf-8')
assert 'Actions' in content_t, "'Actions' column not found in teacher_allocation"
assert 'fa-eye' in content_t, "'fa-eye' view icon not found in teacher_allocation"
assert 'fa-pen-to-square' in content_t, "'fa-pen-to-square' edit icon not found in teacher_allocation"
assert 'fa-trash-can' in content_t, "'fa-trash-can' delete icon not found in teacher_allocation"
assert 'showViewModal' in content_t, "View modal not found in teacher_allocation"
assert 'showEditModal' in content_t, "Edit modal not found in teacher_allocation"
assert 'showDeleteModal' in content_t, "Delete modal not found in teacher_allocation"
print("[OK] Teacher Class Allocation page renders Actions column with View, Edit, Delete modals and icons")

# 3. Test Student Allocation Edit & Delete POST
student = User.objects.filter(role__role_name='Student').first() or user
batch1 = Batch.objects.first()
batch2 = Batch.objects.exclude(batch_id=batch1.batch_id).first() or batch1

# Create a test StudentEnrollment
test_enroll = StudentEnrollment.objects.create(
    student=student,
    course=batch1.course,
    batch=batch1,
    status=1
)
print(f"Created test enrollment id {test_enroll.enrollment_id} with batch {batch1.batch_name}")

# Test Edit POST
resp_edit = client.post('/student-allocation/', {
    'action': 'edit_student_allocation',
    'enrollment_id': test_enroll.enrollment_id,
    'student_id': student.user_id,
    'batch_id': batch2.batch_id
}, follow=True)
test_enroll.refresh_from_db()
print(f"After edit, enrollment batch_id: {test_enroll.batch_id} (expected: {batch2.batch_id})")
assert test_enroll.batch_id == batch2.batch_id, "Edit failed to update batch!"
print("[OK] Student allocation Edit functionality passed!")

# Test Delete POST
resp_del = client.post('/student-allocation/', {
    'action': 'delete_student_allocation',
    'enrollment_id': test_enroll.enrollment_id
}, follow=True)
exists = StudentEnrollment.objects.filter(enrollment_id=test_enroll.enrollment_id).exists()
print(f"After delete, enrollment exists: {exists}")
assert not exists, "Delete failed to remove enrollment record!"
print("[OK] Student allocation Delete functionality passed!")

# 4. Test Teacher Allocation Edit & Delete POST
teacher1 = User.objects.filter(role__role_name='Teacher').first() or user
teacher2 = User.objects.filter(role__role_name='Teacher').exclude(user_id=teacher1.user_id).first() or teacher1

# Create or use a test batch
course = Course.objects.first()
test_batch = Batch.objects.create(
    batch_name="Test Allocation Batch",
    batch_code="TB-999",
    course=course,
    teacher=teacher1,
    is_active=True
)
print(f"Created test batch {test_batch.batch_id} with teacher {teacher1.display_name}")

# Test Edit POST
resp_t_edit = client.post('/teacher-allocation/', {
    'action': 'edit_teacher_allocation',
    'batch_id': test_batch.batch_id,
    'teacher_id': teacher2.user_id
}, follow=True)
test_batch.refresh_from_db()
print(f"After edit, batch teacher_id: {test_batch.teacher_id} (expected: {teacher2.user_id})")
assert test_batch.teacher_id == teacher2.user_id, "Edit failed to reassign teacher!"
print("[OK] Teacher allocation Edit functionality passed!")

# Test Delete POST
resp_t_del = client.post('/teacher-allocation/', {
    'action': 'delete_teacher_allocation',
    'batch_id': test_batch.batch_id
}, follow=True)
test_batch.refresh_from_db()
print(f"After delete, batch teacher: {test_batch.teacher}")
assert test_batch.teacher is None, "Delete failed to unassign teacher from batch!"
print("[OK] Teacher allocation Delete functionality passed!")

# Clean up test batch
test_batch.delete()

print("\n=== ALL ALLOCATION ACTION VERIFICATIONS PASSED SUCCESSFULLY! ===")
