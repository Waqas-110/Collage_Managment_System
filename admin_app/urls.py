from django.urls import path, include
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('manage_subjects/', views.manage_subjects, name='manage_subjects'),
    path('student_app/', include('student_app.urls')),

    path('edit_subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('login/', views.custom_login, name='custom_login'),

    path('logout/', views.custom_logout, name='custom_logout'),
]