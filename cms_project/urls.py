from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from admin_app.views import custom_login

urlpatterns = [
    path('', custom_login, name='home'),
    path('admin/', admin.site.urls),
    path('admin_app/', include('admin_app.urls')),
    path('teacher_app/', include('teacher_app.urls')),
    path('student_app/', include('student_app.urls')),
    path('course_app/', include('course_app.urls')),  
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])