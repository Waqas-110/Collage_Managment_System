# admin_app/admin.py
from django.contrib import admin
# Import all models that are defined in admin_app/models.py
# ✅ RIGHT (agar sirf AdminProfile aur StaffProfile hi hain)
from .models import AdminProfile, StaffProfile, Course, Subject, Session, LeaveApplication, Feedback

# Register your models here.
admin.site.register(AdminProfile)
admin.site.register(StaffProfile)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(LeaveApplication)
admin.site.register(Feedback)