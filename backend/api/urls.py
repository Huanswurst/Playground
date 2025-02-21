from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Admin routes
router.register('admin/staff', views.StaffManagementViewSet, basename='admin-staff')
router.register('admin/courses', views.CourseManagementViewSet, basename='admin-courses')
router.register('admin/students', views.StudentManagementViewSet, basename='admin-students')
router.register('admin/attendance-events', views.AttendanceEventManagementViewSet, basename='admin-attendance-events')
router.register('admin/attendance-records', views.AttendanceRecordManagementViewSet, basename='admin-attendance-records')
router.register('admin/course-participants', views.CourseParticipantManagementViewSet, basename='admin-course-participants')

# Teacher routes
router.register('teacher/courses', views.TeacherCourseViewSet, basename='teacher-courses')
router.register('teacher/attendance-events', views.TeacherAttendanceEventViewSet, basename='teacher-attendance-events')

# Student routes
router.register('student/courses', views.StudentCourseViewSet, basename='student-courses')
router.register('student/attendance-events', views.StudentAttendanceEventViewSet, basename='student-attendance-events')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('current_user/', views.current_user, name='current_user'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_api, name='test_api'),
]
