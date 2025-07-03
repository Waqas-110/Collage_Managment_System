from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.student_home, name='student_home'),
    path('view-attendance/', views.view_attendance, name='student_view_attendance'),
    path('view-marks/', views.view_marks, name='student_view_marks'),
]