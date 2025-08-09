### accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_teacher(self):
        return self.user_type == 'teacher'

    def is_student(self):
        return self.user_type == 'student'
