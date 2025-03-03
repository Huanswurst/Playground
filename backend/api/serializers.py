from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Student, Staff, Course, AttendanceEvent, AttendanceRecord, CourseParticipant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'display_name', 'role', 'last_login', 'created_at')
        read_only_fields = ('last_login', 'created_at')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'display_name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            display_name=validated_data.get('display_name', ''),
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(
        source='students.count',
        read_only=True,
        help_text='Number of enrolled students'
    )
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Student.objects.all(),
        required=False
    )

    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'students': {'write_only': True}
        }

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)
        return expanded_fields + ['student_count']

class AttendanceEventSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = AttendanceEvent
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    event = AttendanceEventSerializer(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'

class CourseParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseParticipant
        fields = '__all__'

class CourseParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = ('user', 'course', 'role')

    def validate(self, data):
        user = data['user']
        course = data['course']
        role = data['role']
        
        if role == 'teacher' and user.role != 'teacher':
            raise serializers.ValidationError("Only teachers can be assigned as course teachers")
        if role == 'student' and user.role != 'student':
            raise serializers.ValidationError("Only students can be enrolled as course students")
            
        return data
