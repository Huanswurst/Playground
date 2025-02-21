from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from .models import User, Student, Staff, Course, AttendanceEvent, AttendanceRecord, CourseParticipant
from .serializers import *

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

# Admin views
class StaffManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class CourseManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AttendanceEventManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = AttendanceEvent.objects.all()
    serializer_class = AttendanceEventSerializer

class AttendanceRecordManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

class CourseParticipantManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CourseParticipant.objects.all()
    serializer_class = CourseParticipantSerializer

# Teacher views
class TeacherCourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(
            courseparticipant__user=self.request.user,
            courseparticipant__role='teacher'
        )

class TeacherAttendanceEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceEventSerializer

    def get_queryset(self):
        return AttendanceEvent.objects.filter(
            course__courseparticipant__user=self.request.user,
            course__courseparticipant__role='teacher'
        )

# Student views
class StudentCourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(
            courseparticipant__user=self.request.user,
            courseparticipant__role='student'
        )

class StudentAttendanceEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceEventSerializer

    def get_queryset(self):
        return AttendanceEvent.objects.filter(
            course__courseparticipant__user=self.request.user,
            course__courseparticipant__role='student'
        )

# Test API
@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API is working!',
        'status': 'success'
    })
