from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView

router = DefaultRouter()
# 公共路由
router.register('courses', views.CourseManagementViewSet, basename='courses')

# Admin routes
router.register('admin/staff', views.StaffManagementViewSet, basename='admin-staff')
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

# 班级管理路由
router.register('admin/classes', views.ClassViewSet, basename='admin-classes')
router.register('admin/class-students', views.ClassStudentViewSet, basename='admin-class-students')
router.register('admin/class-teachers', views.ClassTeacherViewSet, basename='admin-class-teachers')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('current_user/', views.current_user, name='current_user'),
    path('user/me/', views.current_user, name='current_user_me'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test_api, name='test_api'),
    path('face/match/', views.FaceMatchAPI.as_view(), name='face-match'),
    path('face/register/', views.FaceRegistrationAPI.as_view(), name='face-register'),
    
    # 学生相关API
    path('student/dashboard/', views.StudentDashboardAPI.as_view(), name='student-dashboard'),
    path('student/geo-attendance/', views.GeoFaceRecognitionAttendanceAPI.as_view(), name='geo-attendance'),
    path('student/photo-recognition/', views.PhotoRecognitionAPI.as_view(), name='photo-recognition'),
    path('student/selfie-capture/', views.StudentSelfieCaptureAPI.as_view(), name='selfie-capture'),
    
    # 教师相关API
    path('teacher/dashboard/', views.TeacherDashboardAPI.as_view(), name='teacher-dashboard'),
    path('teacher/group-photo/', views.GroupPhotoCaptureAPI.as_view(), name='group-photo'),
    
    # 管理员相关API
    path('admin/attendance/', views.AttendanceManagementAPI.as_view(), name='attendance-management'),
    path('admin/statistics/', views.DataStatisticsAPI.as_view(), name='data-statistics'),
    path('admin/logs/', views.LogManagementAPI.as_view(), name='log-management'),
    path('admin/permissions/', views.PermissionManagementAPI.as_view(), name='permission-management'),
    path('admin/settings/', views.SystemSettingsAPI.as_view(), name='system-settings'),
    path('change-password/', views.ChangePasswordAPI.as_view(), name='change_password'),
    
    # 对象识别API
    path('object-recognition/', views.ObjectRecognitionAPI.as_view(), name='object-recognition'),
    
    # 用户信息API
    path('users/<int:pk>/', views.UserDetailAPI.as_view(), name='user-detail'),
    # 密码修改API
    path('users/change-password/', views.ChangePasswordAPI.as_view(), name='change-password'),
]
