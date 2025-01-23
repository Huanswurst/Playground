from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import *
from django.core.files.base import ContentFile
import base64
import json

# Authentication views
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)

# Face Recognition APIs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_face_data(request):
    try:
        student = Student.objects.get(user=request.user)
        face_data = request.data.get('face_encoding')
        
        if not face_data:
            return Response({'error': 'Face encoding is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        FaceRecognitionData.objects.update_or_create(
            student=student,
            defaults={'face_encoding': base64.b64decode(face_data)}
        )
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Attendance APIs
class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Attendance.objects.filter(course__teacher=user.teacher)
        elif hasattr(user, 'student'):
            return Attendance.objects.filter(student=user.student)
        return Attendance.objects.none()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if hasattr(request.user, 'student'):
            data['student'] = request.user.student.id
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# System Settings APIs
class SystemSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SystemSettingsSerializer
    queryset = SystemSettings.objects.all()

    def get_queryset(self):
        key = self.request.query_params.get('key', None)
        if key:
            return self.queryset.filter(key=key)
        return self.queryset

# Admin Management Views
class ClassManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class CourseManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

# Test API
@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API is working!',
        'status': 'success'
    })
