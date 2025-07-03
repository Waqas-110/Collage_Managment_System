from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, default="DEFAULT-CODE")
    description = models.TextField()
    timing = models.CharField(
        max_length=100,  # Increased to store multiple values
        default="morning"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name