from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Student
from .serializers import FaceMatchSerializer
import numpy as np
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum, Avg
from .models import User, Student, Staff, Course, AttendanceEvent, AttendanceRecord, CourseParticipant, SystemLog
from .serializers import *
# import face_recognition
import numpy as np
import tempfile
import os
from datetime import datetime, timedelta

# 学生仪表盘API
class StudentDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        courses = Course.objects.filter(students=student)
        attendance = AttendanceRecord.objects.filter(student=student)
        
        data = {
            'total_courses': courses.count(),
            'total_attendance': attendance.count(),
            'attendance_rate': round(attendance.filter(status='present').count() / max(attendance.count(), 1) * 100, 2)
        }
        return Response(data)

# 地理位置人脸识别考勤API
class GeoFaceRecognitionAttendanceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 获取地理位置和人脸数据
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            face_descriptor = np.array(request.data.get('descriptor'))

            # 验证地理位置
            if not all([latitude, longitude]):
                return Response({'error': '缺少地理位置信息'}, status=status.HTTP_400_BAD_REQUEST)

            # 人脸识别逻辑
            student = Student.objects.get(user=request.user)
            stored_descriptor = np.frombuffer(student.face_embedding, dtype=np.float32)
            distance = np.linalg.norm(face_descriptor - stored_descriptor)
            
            if distance > 0.6:
                return Response({'error': '人脸验证失败'}, status=status.HTTP_401_UNAUTHORIZED)

            # 记录考勤
            event = AttendanceEvent.objects.filter(
                course__students=student,
                start_time__lte=datetime.now(),
                end_time__gte=datetime.now()
            ).first()

            if not event:
                return Response({'error': '当前没有进行中的考勤事件'}, status=status.HTTP_404_NOT_FOUND)

            AttendanceRecord.objects.create(
                event=event,
                student=student,
                status='present',
                location=f"{latitude},{longitude}"
            )

            return Response({'message': '考勤成功'})

        except Student.DoesNotExist:
            return Response({'error': '学生信息不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 照片识别API
class PhotoRecognitionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            photo_file = request.FILES.get('photo')
            if not photo_file:
                return Response({'error': '缺少照片文件'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存照片
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                for chunk in photo_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # 人脸识别逻辑
            image = face_recognition.load_image_file(temp_file_path)
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return Response({'error': '未检测到人脸'}, status=status.HTTP_400_BAD_REQUEST)

            # 返回识别结果
            return Response({
                'face_count': len(face_locations),
                'face_locations': face_locations
            })

        finally:
            os.unlink(temp_file_path)

# 学生自拍捕获API
class StudentSelfieCaptureAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            photo_file = request.FILES.get('photo')
            if not photo_file:
                return Response({'error': '缺少照片文件'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存照片
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                for chunk in photo_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # 人脸识别逻辑
            image = face_recognition.load_image_file(temp_file_path)
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return Response({'error': '未检测到人脸'}, status=status.HTTP_400_BAD_REQUEST)

            # 更新学生人脸数据
            student = Student.objects.get(user=request.user)
            face_descriptor = face_recognition.face_encodings(image)[0]
            student.face_embedding = face_descriptor.tobytes()
            student.save()

            return Response({'message': '人脸数据更新成功'})

        except Student.DoesNotExist:
            return Response({'error': '学生信息不存在'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            os.unlink(temp_file_path)

# 教师仪表盘API
class TeacherDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = Staff.objects.get(user=request.user)
        courses = Course.objects.filter(teacher=teacher)
        attendance = AttendanceEvent.objects.filter(course__teacher=teacher)
        
        data = {
            'total_courses': courses.count(),
            'total_students': Student.objects.filter(courses__teacher=teacher).distinct().count(),
            'total_attendance_events': attendance.count()
        }
        return Response(data)

# 集体照片捕获API
class GroupPhotoCaptureAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            photo_file = request.FILES.get('photo')
            course_id = request.data.get('course_id')
            
            if not all([photo_file, course_id]):
                return Response({'error': '缺少必要参数'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存照片
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                for chunk in photo_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # 人脸识别逻辑
            image = face_recognition.load_image_file(temp_file_path)
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return Response({'error': '未检测到人脸'}, status=status.HTTP_400_BAD_REQUEST)

            # 返回识别结果
            return Response({
                'face_count': len(face_locations),
                'face_locations': face_locations
            })

        finally:
            os.unlink(temp_file_path)

# 数据统计API
class DataStatisticsAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取系统统计数据
        total_students = Student.objects.count()
        total_teachers = Staff.objects.count()
        total_courses = Course.objects.count()
        total_attendance = AttendanceRecord.objects.count()

        # 获取最近7天的数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        attendance_data = AttendanceRecord.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('created_at__date').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='present'))
        )

        return Response({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_attendance': total_attendance,
            'attendance_data': attendance_data
        })

# 日志管理API
class LogManagementAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = SystemLog.objects.all().order_by('-created_at')[:100]
        serializer = SystemLogSerializer(logs, many=True)
        return Response(serializer.data)

# 权限管理API
class PermissionManagementAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserPermissionSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user_id')
        permissions = request.data.get('permissions')
        
        try:
            user = User.objects.get(id=user_id)
            user.user_permissions.set(permissions)
            return Response({'message': '权限更新成功'})
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

# 系统设置API
class AttendanceManagementAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取查询参数
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        user_type = request.query_params.get('user_type')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        # 构建基础查询
        queryset = AttendanceRecord.objects.all().order_by('-created_at')

        # 应用日期过滤
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # 应用用户类型过滤
        if user_type == 'student':
            queryset = queryset.filter(student__isnull=False)
        elif user_type == 'teacher':
            queryset = queryset.filter(teacher__isnull=False)

        # 分页处理
        total_count = queryset.count()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        records = queryset[start_index:end_index]

        # 序列化数据
        serializer = AttendanceRecordSerializer(records, many=True)

        return Response({
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })

class SystemSettingsAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = SystemSettings.objects.first()
        serializer = SystemSettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        settings = SystemSettings.objects.first()
        serializer = SystemSettingsSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '系统设置更新成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 对象识别API
class ObjectRecognitionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            photo_file = request.FILES.get('photo')
            if not photo_file:
                return Response({'error': '缺少照片文件'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存照片
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                for chunk in photo_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # 对象识别逻辑
            # 这里需要实现具体的对象识别逻辑
            # 返回识别结果
            return Response({
                'objects': []  # 返回识别到的对象列表
            })

        finally:
            os.unlink(temp_file_path)

class StaffManagementViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.request.query_params.get('position', None)
        if position:
            queryset = queryset.filter(position=position)
        return queryset

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        staff = self.get_object()
        staff.user.is_active = False
        staff.user.save()
        return Response({'status': 'deactivated'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        staff = self.get_object()
        staff.user.is_active = True
        staff.user.save()
        return Response({'status': 'activated'})

class CourseManagementViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        course = self.get_object()
        course.is_active = True
        course.save()
        return Response({'status': 'activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        course = self.get_object()
        course.is_active = False
        course.save()
        return Response({'status': 'deactivated'})

class StudentManagementViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        student = self.get_object()
        student.user.is_active = True
        student.user.save()
        return Response({'status': 'activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        student = self.get_object()
        student.user.is_active = False
        student.user.save()
        return Response({'status': 'deactivated'})

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade', None)
        major = self.request.query_params.get('major', None)
        
        if grade:
            queryset = queryset.filter(grade=grade)
        if major:
            queryset = queryset.filter(major=major)
        return queryset

class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 创建用户并分配角色
            user = serializer.save()
            
            # 根据角色创建关联模型
            role = serializer.validated_data.get('role', 'student')
            if role == 'student':
                Student.objects.create(user=user)
            elif role == 'teacher':
                Staff.objects.create(user=user)
            elif role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()

            # 生成认证token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'role': role
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"注册失败: {str(e)}")
            return Response(
                {'error': '用户注册失败，请检查输入数据'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ClassStudentViewSet(viewsets.ModelViewSet):
    queryset = ClassStudent.objects.all()
    serializer_class = ClassStudentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id', None)
        
        if class_id:
            queryset = queryset.filter(class_instance=class_id)
        return queryset

class ClassTeacherViewSet(viewsets.ModelViewSet):
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get('class_id', None)
        
        if class_id:
            queryset = queryset.filter(class_instance=class_id)
        return queryset

class StudentManagementViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        student = self.get_object()
        student.user.is_active = True
        student.user.save()
        return Response({'status': 'activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        student = self.get_object()
        student.user.is_active = False
        student.user.save()
        return Response({'status': 'deactivated'})

class AttendanceEventManagementViewSet(viewsets.ModelViewSet):
    queryset = AttendanceEvent.objects.all()
    serializer_class = AttendanceEventSerializer
    permission_classes = [IsAdminUser]

class AttendanceRecordManagementViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAdminUser]

class CourseParticipantManagementViewSet(viewsets.ModelViewSet):
    queryset = CourseParticipant.objects.all()
    serializer_class = CourseParticipantSerializer
    permission_classes = [IsAdminUser]

class TeacherCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(teacher__user=self.request.user)

class TeacherAttendanceEventViewSet(viewsets.ModelViewSet):
    queryset = AttendanceEvent.objects.all()
    serializer_class = AttendanceEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(course__teacher__user=self.request.user)

class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(students__user=self.request.user)

class StudentAttendanceEventViewSet(viewsets.ModelViewSet):
    queryset = AttendanceEvent.objects.all()
    serializer_class = AttendanceEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(course__students__user=self.request.user)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not all([username, password]):
        return Response({'error': '缺少用户名或密码'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        auth_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
    else:
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    auth_logout(request)
    return Response({'message': '成功登出'})

@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        })
    return Response({'error': '用户未登录'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def test_api(request):
    return Response({'message': 'API测试成功'})

class FaceMatchAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            face_descriptor = np.array(request.data.get('descriptor'))
            student = Student.objects.get(user=request.user)
            stored_descriptor = np.frombuffer(student.face_embedding, dtype=np.float32)
            distance = np.linalg.norm(face_descriptor - stored_descriptor)
            
            if distance > 0.6:
                return Response({'error': '人脸验证失败'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'message': '人脸验证成功'})
        except Student.DoesNotExist:
            return Response({'error': '学生信息不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FaceRegistrationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            face_descriptor = np.array(request.data.get('descriptor'))
            student = Student.objects.get(user=request.user)
            student.face_embedding = face_descriptor.tobytes()
            student.save()
            return Response({'message': '人脸注册成功'})
        except Student.DoesNotExist:
            return Response({'error': '学生信息不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
