from rest_framework import serializers
from .models import (
    User,
    Student,
    Staff,
    Course,
    AttendanceEvent,
    AttendanceRecord,
    CourseParticipant,
    SystemLog,
    Class,
    ClassStudent,
    ClassTeacher
)
import numpy as np

class FaceMatchSerializer(serializers.Serializer):
    descriptor = serializers.ListField(
        child=serializers.FloatField(),
        min_length=128,
        max_length=128
    )

    def validate_descriptor(self, value):
        if len(value) != 128:
            raise serializers.ValidationError("人脸特征维度必须为128维")
        return np.array(value, dtype=np.float32)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'display_name', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'display_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            display_name=validated_data['display_name'],
            role=validated_data.get('role', 'student'),
            password=validated_data['password']
        )
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'student_number']

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ['user', 'employee_number', 'position']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'course_code', 'course_name', 'academic_year', 'semester']

class AttendanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceEvent
        fields = ['event_id', 'course', 'release_time', 'deadline', 'auth_method']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['record_id', 'student', 'event', 'status', 'created_at']

class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = ['student', 'course', 'role', 'enrolled_at']

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = ['level', 'message', 'created_at', 'user', 'related_object_type', 'related_object_id']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_id', 'class_name', 'grade', 'major', 'created_at', 'updated_at']

class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStudent
        fields = ['class_instance', 'student', 'enrolled_at']

class ClassTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTeacher
        fields = ['class_instance', 'teacher', 'assigned_at']
