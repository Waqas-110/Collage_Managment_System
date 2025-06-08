from django.db import models
from django.contrib.auth.models import User

# Admin Profile Model
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

# Staff Profile Model
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.full_name

# Student Model
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Session Model
class Session(models.Model):
    session_start = models.DateField()
    session_end = models.DateField()

    def __str__(self):
        return f"{self.session_start} - {self.session_end}"

# Leave Application Model
class LeaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Leave - {self.user.username}"

# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"


