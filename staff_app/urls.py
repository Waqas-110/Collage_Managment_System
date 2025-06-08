# staff_app/urls.py
from django.urls import path
from . import views

app_name = 'staff_app'  # Add this line to define the namespace

urlpatterns = [
    path('staff_home/', views.staff_home, name='staff_home'),
    # other staff_app URL patterns...

  # ✅ staff login URL
    path('home/', views.staff_home, name='staff_home'),
]
