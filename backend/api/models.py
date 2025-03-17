from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=50, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ])
    
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
        return self.display_name or self.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    face_embedding = models.BinaryField(null=True, blank=True)  # 使用BinaryField存储二进制特征数据
    face_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.display_name} ({self.student_number})"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_number = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=20, choices=[
        ('teacher', 'Teacher'),
        ('administrator', 'Administrator')
    ])

    def __str__(self):
        return f"{self.user.display_name} ({self.employee_number})"

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ])
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'role')
        indexes = [
            models.Index(fields=['course', 'role'])
        ]

    def __str__(self):
        return f"{self.student} - {self.course} ({self.role})"

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
