# student_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Student
from course_app.models import Course





@login_required
def student_home(request):
    return render(request, 'student_app/student_home.html', {'user': request.user})

@login_required
def manage_students(request):
    students = Student.objects.all()
    return render(request, 'student_app/manage_students.html', {'students': students})

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

            if not all([username, password, name, email, phone]):  # Remove course_id from required fields
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

            # Get course instance if course_id is provided
            course = None
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    user.delete()
                    messages.error(request, "Selected course does not exist")
                    return redirect('student_app:add_student')

            # Create Student profile
            Student.objects.create(
                user=user,
                name=name,
                email=email,
                course=course,  # This can be None now
                phone=phone
            )
            messages.success(request, "Student added successfully")
            return redirect('student_app:manage_students')

        except Exception as e:
            if 'user' in locals():
                user.delete()
            messages.error(request, f"Error adding student: {str(e)}")
            return redirect('student_app:add_student')

    courses = Course.objects.all()
    return render(request, 'student_app/add_student.html', {'courses': courses})
@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            course_id = request.POST.get('course')
            phone = request.POST.get('phone')

            # Get the course instance
            course = Course.objects.get(id=course_id)

            student.name = name
            student.email = email
            student.course = course  # Assign the course instance
            student.phone = phone
            student.save()

            messages.success(request, "Student updated successfully!")
            return redirect('student_app:manage_students')
        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist")
        except Exception as e:
            messages.error(request, f"Error updating student: {str(e)}")

    courses = Course.objects.all()
    return render(request, 'student_app/edit_student.html', {
        'student': student,
        'courses': courses
    })
@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('student_app:manage_students')