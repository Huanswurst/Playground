from django.db import migrations
from datetime import datetime, timedelta
import random

def create_test_data(apps, schema_editor):
    # 获取模型
    Student = apps.get_model('api', 'Student')
    Course = apps.get_model('api', 'Course')
    AttendanceEvent = apps.get_model('api', 'AttendanceEvent')
    AttendanceRecord = apps.get_model('api', 'AttendanceRecord')

    # 创建测试学生
    student = Student.objects.create(
        name='测试学生',
        student_id='20230001',
        user_id=1  # 假设用户ID为1
    )

    # 创建测试课程
    courses = []
    for i, name in enumerate(['数学', '英语', '物理', '化学']):
        course = Course.objects.create(
            name=name,
            code=f'C{i+1}',
            description=f'{name}课程'
        )
        courses.append(course)
        course.students.add(student)

    # 创建考勤事件和记录
    statuses = ['present', 'late', 'absent']
    for i in range(30):  # 创建30天的考勤记录
        event_date = datetime.now() - timedelta(days=30 - i)
        for course in courses:
            event = AttendanceEvent.objects.create(
                course=course,
                start_time=event_date.replace(hour=8, minute=0),
                end_time=event_date.replace(hour=10, minute=0)
            )
            
            # 创建考勤记录
            AttendanceRecord.objects.create(
                student=student,
                event=event,
                status=random.choice(statuses)
            )

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_data),
    ]