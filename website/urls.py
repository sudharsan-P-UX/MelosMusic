from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('students/', views.students_view, name='students'),
    path('student-course/', views.student_course_view, name='student_course'),
    path('student-allocation/', views.student_allocation_view, name='student_allocation'),
    path('teacher-allocation/', views.teacher_allocation_view, name='teacher_allocation'),
    path('api/get-teacher/', views.api_get_teacher_details, name='api_get_teacher'),
    path('api/get-student/', views.api_get_student_details, name='api_get_student'),
    path('api/get-batch/', views.api_get_batch_details, name='api_get_batch'),
    path('students/update/<int:student_id>/', views.update_student, name='update_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('teachers/', views.teachers_view, name='teachers'),
    path('teachers/update/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('courses/', views.courses_batches_view, name='courses'),
    path('fees/dashboard/', views.fee_dashboard_view, name='fee_dashboard'),
    path('fees/assign/', views.assign_fees_view, name='assign_fees'),
    path('fees/pending/', views.pending_fees_view, name='pending_fees'),
    path('fees/receipts/', views.receipts_view, name='receipts'),
    path('fees/refunds/', views.refunds_view, name='refunds'),
    path('fees/reports/', views.reports_view, name='reports'),

    path('fees/collection/', views.fee_collection_view, name='fee_collection'),
    path('attendance/student/', views.student_attendance_view, name='student_attendance'),
    path('attendance/teacher/', views.teacher_attendance_view, name='teacher_attendance'),

    path('enrollment_management/', views.enrollment_management_view, name='enrollment_management'),
    path('events/', views.events_dashboard_view, name='events_dashboard'),
    path('events/create/', views.create_event_view, name='create_event'),
    path('page/<str:page_name>/', views.generic_page, name='generic_page'),
]
