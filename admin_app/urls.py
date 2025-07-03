from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.custom_login, name='custom_login'),

    # Dashboard
    path('home/', views.admin_home, name='admin_home'),

    # Student CRUD
    path('students/', views.student_list, name='student_list'),
    path('add-student/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # Teacher CRUD
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),

    # Course CRUD
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    # Analytics
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('predictive-analytics/', views.predictive_analytics, name='predictive_analytics'),
    path('logout/', views.custom_logout, name='custom_logout'),

]
