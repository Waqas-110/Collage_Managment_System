# Import the Django admin module
from django.contrib import admin

# Import the Profile model from the current app's models.py
from .models import Profile

# Register the Profile model to make it visible in the Django admin panel
# Taa ke admin panel me Profile ka section aa jaye, aur data manage kar saken
admin.site.register(Profile)
