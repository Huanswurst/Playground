from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Admin routes
router.register('admin/attendance', views.AttendanceViewSet, basename='admin-attendance')
router.register('admin/classes', views.ClassManagementViewSet, basename='admin-classes')
router.register('admin/courses', views.CourseManagementViewSet, basename='admin-courses')
router.register('admin/students', views.StudentManagementViewSet, basename='admin-students')
router.register('admin/teachers', views.TeacherManagementViewSet, basename='admin-teachers')
router.register('admin/settings', views.SystemSettingsViewSet, basename='admin-settings')

# Teacher routes
router.register('teacher/courses', views.TeacherCourseViewSet, basename='teacher-courses')
router.register('teacher/attendance', views.AttendanceViewSet, basename='teacher-attendance')

# Student routes
router.register('student/attendance', views.AttendanceViewSet, basename='student-attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('current_user/', views.current_user, name='current_user'),
    path('logout/', views.logout_view, name='logout'),
    path('face-recognition/upload/', views.upload_face_data, name='upload-face-data'),
    path('test/', views.test_api, name='test_api'),
]
