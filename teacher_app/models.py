from django.db import models
from django.contrib.auth.models import User
from course_app.models import Subject, Course
from student_app.models import Student

class Teacher(models.Model):
    TIMING_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, default="Teacher")
    last_name = models.CharField(max_length=50, default="User")
    age = models.PositiveIntegerField(default=30)
    email = models.EmailField(default="teacher@example.com")
    courses = models.ManyToManyField(Course, related_name='teachers')
    timing = models.CharField(max_length=100, default="Morning")  # Store as comma-separated values
    profile_picture = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

class StudentMarks(models.Model):
    MARKS_TYPE_CHOICES = [
        ('Midterm', 'Midterm'),
        ('Final', 'Final'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Other', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_for = models.CharField(max_length=20, choices=MARKS_TYPE_CHOICES, default='Midterm')
    marks = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField(default=100)
    exam_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.course.name} - {self.marks_for} - {self.marks}/{self.max_marks}"