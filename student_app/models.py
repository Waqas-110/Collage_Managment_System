from django.db import models
from django.contrib.auth.models import User
from course_app.models import Course  # Make sure you're importing Course from the correct app

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)  # Allow null
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name