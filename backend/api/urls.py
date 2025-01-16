from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/user/', views.current_user, name='current_user'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('test/', views.test_api, name='test_api'),
]
