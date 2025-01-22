from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    classes = models.ManyToManyField(Class)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ])
    recognition_data = models.JSONField(null=True, blank=True)
    location_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'course', 'date')
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} {self.time}"

class FaceRecognitionData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    face_encoding = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student',)
    
    def __str__(self):
        return f"{self.student} - Face Data"

class SystemSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.key} - {self.value}"
