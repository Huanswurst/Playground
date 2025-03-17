from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
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

User = get_user_model()
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
    email = serializers.EmailField(
        required=True,
        help_text="有效的电子邮件地址"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="至少8个字符，包含字母和数字"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'username': {
                'min_length': 4,
                'help_text': "4-20个字符，只能包含字母、数字和下划线"
            }
        }

    def validate(self, data):
        # 新增角色字段验证
        if 'role' not in data:
            raise serializers.ValidationError({"role": "必须选择用户角色"})
        if data['role'] not in ['student', 'teacher', 'admin']:
            raise serializers.ValidationError({"role": "无效的用户角色"})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "该用户名已被使用"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "该邮箱已被注册"})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating user
        validated_data.pop('confirm_password', None)
        
        # 手动处理密码哈希
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'display_name', 'role']

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
