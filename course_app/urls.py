from django.urls import path
from . import views

app_name = 'course_app'

urlpatterns = [
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
]