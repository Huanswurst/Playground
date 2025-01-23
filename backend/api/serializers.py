from rest_framework import serializers
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Attendance, Class, Course, Student, Teacher, FaceRecognitionData, SystemSettings
=======
from django.contrib.auth import get_user_model
from .models import Course, Class, Attendance, Location

User = get_user_model()
>>>>>>> 4d46f07 (添加高德地图安全密钥，优化用户模型，更新考勤和课程相关逻辑，新增底部组件)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_student', 'is_teacher', 'is_admin']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_student', 'is_teacher', 'is_admin']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_student = validated_data.get('is_student', False)
        user.is_teacher = validated_data.get('is_teacher', False)
        user.is_admin = validated_data.get('is_admin', False)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'radius']

class CourseSerializer(serializers.ModelSerializer):
    allowed_location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'teacher', 'start_date', 'end_date', 'allowed_location']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'course', 'date', 'start_time', 'end_time']

class AttendanceSerializer(serializers.ModelSerializer):
    location = serializers.JSONField()
    recognition_data = serializers.CharField()
    
    class Meta:
        model = Attendance
<<<<<<< HEAD
        fields = '__all__'
        extra_kwargs = {
            'recognition_data': {'write_only': True},
            'location_data': {'write_only': True}
        }

class FaceRecognitionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceRecognitionData
        fields = '__all__'
        extra_kwargs = {
            'face_encoding': {'write_only': True}
        }

class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = '__all__'
=======
        fields = ['id', 'student', 'course', 'class_session', 'status', 'timestamp', 'location', 'recognition_data']
        read_only_fields = ['timestamp']

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['course', 'status', 'location', 'recognition_data']
>>>>>>> 4d46f07 (添加高德地图安全密钥，优化用户模型，更新考勤和课程相关逻辑，新增底部组件)
