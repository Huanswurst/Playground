from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('student', '学生'),
        ('teacher', '教师'),
        ('admin', '管理员')
    ], default='student')
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
    
    # Add custom related_names to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    face_embedding = models.BinaryField(null=True, blank=True)
    face_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.display_name or self.user.username} ({self.student_number})"

    @classmethod
    def get_next_student_number(cls):
        from django.db import transaction
        import datetime
        
        current_year = datetime.datetime.now().year
        with transaction.atomic():
            # 使用select_for_update锁定记录防止并发冲突
            last_student = cls.objects.select_for_update().filter(
                student_number__startswith=str(current_year)
            ).order_by('-student_number').first()
            
            if last_student:
                last_seq = int(last_student.student_number[-4:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
                
            return f"{current_year}{new_seq:04d}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    employee_number = models.AutoField(primary_key=True)
    position = models.CharField(max_length=20, choices=[
        ('teacher', 'Teacher'),
        ('administrator', 'Administrator')
    ])

    def __str__(self):
        return f"{self.user.display_name or self.user.username} ({self.employee_number})"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    academic_year = models.SmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    semester = models.CharField(max_length=10, choices=[
        ('spring', 'Spring'),
        ('fall', 'Fall')
    ])
    students = models.ManyToManyField(
        'Student', 
        related_name='courses',
        through='CourseParticipant',
        through_fields=('course', 'student'),
        blank=True
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class AttendanceEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    release_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    auth_method = models.CharField(max_length=20, choices=[
        ('face', 'Face Recognition'),
        ('location', 'Location'),
        ('code', 'Code')
    ])

    def __str__(self):
        return f"{self.course} - {self.release_time}"

class AttendanceRecord(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(AttendanceEvent, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['student', 'event']),
            models.Index(fields=['event', 'status'])
        ]

    def __str__(self):
        return f"{self.student} - {self.event} - {self.status}"

class CourseParticipant(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ])
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('student', 'course', 'role'), ('staff', 'course', 'role')]
        indexes = [
            models.Index(fields=['course', 'role'])
        ]

    def __str__(self):
        if self.student:
            return f"{self.student} - {self.course} ({self.role})"
        elif self.staff:
            return f"{self.staff} - {self.course} ({self.role})"
        return f"Unknown - {self.course} ({self.role})"

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    major = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_name} ({self.grade} {self.major})"

class ClassStudent(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('class_instance', 'student')
        indexes = [
            models.Index(fields=['class_instance', 'student'])
        ]

    def __str__(self):
        return f"{self.student} in {self.class_instance}"

class ClassTeacher(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('class_instance', 'teacher')
        indexes = [
            models.Index(fields=['class_instance', 'teacher'])
        ]

    def __str__(self):
        return f"{self.teacher} teaches {self.class_instance}"

class SystemLog(models.Model):
    LOG_LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical')
    ]

    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['level']),
            models.Index(fields=['related_object_type', 'related_object_id'])
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"
