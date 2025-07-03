from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.teacher_home, name='teacher_home'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),
    path('edit-attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    path('give-marks/', views.give_marks, name='give_marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
    path('edit-marks/<int:marks_id>/', views.edit_marks, name='edit_marks'),
]