
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('custom_login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_app/', include('admin_app.urls')),
    path('student/', include('student_app.urls')),
    path('staff/', include('staff_app.urls')),
    path('course_app/', include('course_app.urls')),
    # Add this line for the root URL
    path('', redirect_to_login, name='home'),
]