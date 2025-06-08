from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"
