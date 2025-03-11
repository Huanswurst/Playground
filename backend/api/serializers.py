from rest_framework import serializers
from .models import Student, Staff, Course, AttendanceEvent, AttendanceRecord, User, CourseParticipant
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

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AttendanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceEvent
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = '__all__'
