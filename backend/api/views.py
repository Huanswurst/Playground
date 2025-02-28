from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import User, Student, Staff, Course, AttendanceEvent, AttendanceRecord, CourseParticipant
from .serializers import *
import face_recognition
import numpy as np
import tempfile
import os

# 特殊情况信息录入API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def special_case_enrollment(request):
    try:
        # 获取表单数据
        name = request.POST.get('name')
        student_number = request.POST.get('studentNumber')
        class_name = request.POST.get('class')
        photo_file = request.FILES.get('photo')
        
        if not all([name, student_number, class_name, photo_file]):
            return Response({'error': '缺少必要参数'}, status=status.HTTP_400_BAD_REQUEST)

        # 保存照片
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            for chunk in photo_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # 处理照片（可选）
        try:
            image = face_recognition.load_image_file(temp_file_path)
            face_locations = face_recognition.face_locations(image)
            
            if len(face_locations) == 0:
                return Response({'error': '未检测到人脸'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'照片处理失败: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            os.unlink(temp_file_path)

        # 创建学生记录（示例）
        student = Student.objects.create(
            user=request.user,
            student_number=student_number,
            # 其他字段...
        )

        return Response({'message': '信息录入成功'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 其他已有API保持不变...
