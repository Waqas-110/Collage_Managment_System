from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)  # Optional description field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']