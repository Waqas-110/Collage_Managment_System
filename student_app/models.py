from django.db import models
from django.contrib.auth.models import User
from course_app.models import Course

class Student(models.Model):
    TIMING_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, default="Student")
    last_name = models.CharField(max_length=50, default="User")
    age = models.PositiveIntegerField(default=18)
    email = models.EmailField(default="student@example.com")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    timing = models.CharField(max_length=20, choices=TIMING_CHOICES, default="Morning")
    profile_picture = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"