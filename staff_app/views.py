from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Staff  # Add this import

@login_required
def staff_home(request):
    try:
        staff = Staff.objects.get(admin=request.user)
        return render(request, 'staff_app/staff_home.html', {
            'staff': staff,
            'user': request.user
        })
    except Staff.DoesNotExist:
        messages.error(request, "Staff profile not found")
        return redirect('custom_login')

def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'staff'):
            login(request, user)
            return redirect('staff_app:staff_home')
        else:
            messages.error(request, "Invalid login credentials or not a staff member.")

    return render(request, 'admin_app/login.html')


def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Check if user exists and is a staff member
        if user is not None and hasattr(user, 'staff'):
            login(request, user)
            return redirect('staff_app:staff_home')
        else:
            messages.error(request, "Invalid login credentials or not a staff member.")

    return render(request, 'admin_app/login.html')