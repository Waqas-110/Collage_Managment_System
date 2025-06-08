from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie  # Add this import

# Rest of your imports...
# Models
from student_app.models import Student
from .models import StaffProfile, Course, Subject, AdminProfile, LeaveApplication, Feedback
from staff_app.models import Staff

# =================== LOGIN & LOGOUT ===================

@ensure_csrf_cookie
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # Check if user is superuser
            if user.is_superuser:
                return redirect('admin_home')
            # Check if user is staff by checking staff profile existence
            elif hasattr(user, 'staff'):
                return redirect('staff_app:staff_home')
            # Check if user is student by checking student profile existence
            elif hasattr(user, 'student'):
                return redirect('student_app:student_home')
            else:
                messages.error(request, "Invalid user type")
                return redirect('custom_login')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_app/login.html', {'form': form})
def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('custom_login')

# =================== ADMIN HOME ===================

@login_required
def admin_home(request):
    from student_app.models import Student
    from staff_app.models import Staff
    from .models import Course, Subject

    student_count = Student.objects.count()
    staff_count = Staff.objects.count()
    course_count = Course.objects.count()
    subject_count = Subject.objects.count()

    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
    }
    return render(request, 'admin_app/admin_home.html', context)
@login_required
def manage_staff(request):
    staffs = StaffProfile.objects.all()
    return render(request, 'admin_app/manage_staff.html', {'staffs': staffs})


@login_required
def add_staff(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')

            # Basic validation
            if not all([username, email, password, first_name, last_name, address]):
                messages.error(request, "All fields are required")
                return redirect('add_staff')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('add_staff')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            Staff.objects.create(admin=user, address=address)
            messages.success(request, "Staff added successfully")
            return redirect('manage_staff')

        except Exception as e:
            messages.error(request, f"Error adding staff: {str(e)}")
            return redirect('add_staff')

    # Handle GET request
    return render(request, 'admin_app/add_staff.html')
@login_required
def delete_staff(request, staff_id):
    try:
        staff = Staff.objects.get(id=staff_id)
        user = staff.admin  # Get the associated user
        staff.delete()  # Delete staff profile
        user.delete()  # Delete the user account
        messages.success(request, "Staff deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting staff: {str(e)}")
    return redirect('manage_staff')
# =================== SUBJECTS ===================

@login_required
def add_subject(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            course_id = request.POST.get('course')

            # Basic validation
            if not all([name, course_id]):
                messages.error(request, "All fields are required")
                return redirect('add_subject')

            course = Course.objects.get(id=course_id)
            Subject.objects.create(
                name=name,
                course=course
            )
            messages.success(request, "Subject added successfully")
            return redirect('manage_subjects')

        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist")
            return redirect('add_subject')
        except Exception as e:
            messages.error(request, f"Error adding subject: {str(e)}")
            return redirect('add_subject')

    # For GET request
    courses = Course.objects.all()
    return render(request, 'admin_app/add_subject.html', {'courses': courses})
def manage_staff(request):
    staffs = Staff.objects.all()  # Use Staff instead of StaffProfile
    return render(request, 'admin_app/manage_staff.html', {'staffs': staffs})

# =================== STUDENTS ===================

@login_required
def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'admin_app/manage_subjects.html', {
        'subjects': subjects
    })

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.phone = request.POST['phone']
        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect('manage_students')

    return render(request, 'admin_app/edit_student.html', {'student': student})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('manage_students')


@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            course_id = request.POST.get('course')

            # Basic validation
            if not all([name, course_id]):
                messages.error(request, "All fields are required")
                return redirect('edit_subject', subject_id=subject_id)

            course = Course.objects.get(id=course_id)

            subject.name = name
            subject.course = course
            subject.save()

            messages.success(request, "Subject updated successfully")
            return redirect('manage_subjects')

        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist")
            return redirect('edit_subject', subject_id=subject_id)
        except Exception as e:
            messages.error(request, f"Error updating subject: {str(e)}")
            return redirect('edit_subject', subject_id=subject_id)

    # For GET request
    courses = Course.objects.all()
    return render(request, 'admin_app/edit_subject.html', {
        'subject': subject,
        'courses': courses
    })

@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting subject: {str(e)}")
    return redirect('manage_subjects')


@login_required
def add_student(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name')
            email = request.POST.get('email')
            course_id = request.POST.get('course')
            phone = request.POST.get('phone')

            if not all([username, password, name, email, course_id, phone]):
                messages.error(request, "All fields are required")
                return redirect('student_app:add_student')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('student_app:add_student')

            # Create User account first
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name
            )

            # Get course instance
            course = Course.objects.get(id=course_id)

            # Create Student profile
            Student.objects.create(
                user=user,
                name=name,
                email=email,
                course=course,
                phone=phone
            )
            messages.success(request, "Student added successfully")
            return redirect('student_app:manage_students')  # Make sure this matches your URL name

        except Course.DoesNotExist:
            if 'user' in locals():
                user.delete()
            messages.error(request, "Selected course does not exist")
            return redirect('student_app:add_student')
        except Exception as e:
            if 'user' in locals():
                user.delete()
            messages.error(request, f"Error adding student: {str(e)}")
            return redirect('student_app:add_student')

    courses = Course.objects.all()
    return render(request, 'student_app/add_student.html', {'courses': courses})