from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .decorators import role_required
from student_app.forms import AddStudentForm
from teacher_app.forms import AddTeacherForm
from course_app.forms import AddCourseForm

from student_app.models import Student
from teacher_app.models import Teacher
from course_app.models import Course

import random

# -------------------------------
# Authentication Views
# -------------------------------
def custom_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check user role and redirect accordingly
            if user_type == 'admin':
                if user.is_staff or user.is_superuser:
                    return redirect('admin_home')
                else:
                    error = 'You are not authorized as admin.'
            elif user_type == 'teacher':
                try:
                    teacher = Teacher.objects.get(user=user)
                    return redirect('teacher_home')
                except Teacher.DoesNotExist:
                    error = 'You are not registered as a teacher.'
            elif user_type == 'student':
                try:
                    student = Student.objects.get(user=user)
                    return redirect('student_home')
                except Student.DoesNotExist:
                    error = 'You are not registered as a student.'
            else:
                error = 'Invalid user type selected.'
        else:
            error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})

def custom_logout(request):
    logout(request)
    return redirect('custom_login')

# -------------------------------
# Admin Dashboard
# -------------------------------
@login_required
@role_required('admin')
def admin_home(request):
    return render(request, 'admin_app/admin_home.html', {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_courses': Course.objects.count(),
    })

# -------------------------------
# Student CRUD
# -------------------------------
@login_required
@role_required('admin')
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES)
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif form.is_valid():
            user = User.objects.create_user(
                username=username, 
                password=password,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            student = form.save(commit=False)
            student.user = user
            student.student_id = f"S-{random.randint(1000, 9999)}"
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect('admin_home')
    else:
        student_id = f"S-{random.randint(1000, 9999)}"
        form = AddStudentForm(initial={'student_id': student_id})

    return render(request, 'admin_app/add_student.html', {'form': form})

@login_required
@role_required('admin')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = AddStudentForm(request.POST or None, request.FILES or None, instance=student)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    return render(request, 'admin_app/edit_student.html', {'form': form})

@login_required
@role_required('admin')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')

# -------------------------------
# Teacher CRUD
# -------------------------------
@login_required
@role_required('admin')
def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST, request.FILES)
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif form.is_valid():
            user = User.objects.create_user(
                username=username, 
                password=password,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.teacher_id = form.cleaned_data['teacher_id'] or f"T-{random.randint(1000, 9999)}"
            teacher.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Teacher added successfully!')
            return redirect('admin_home')
    else:
        teacher_id = f"T-{random.randint(1000, 9999)}"
        form = AddTeacherForm(initial={'teacher_id': teacher_id})

    return render(request, 'admin_app/add_teacher.html', {'form': form})

@login_required
@role_required('admin')
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    form = AddTeacherForm(request.POST or None, request.FILES or None, instance=teacher)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_list')

    return render(request, 'admin_app/edit_teacher.html', {'form': form})

@login_required
@role_required('admin')
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    teacher.delete()
    user.delete()
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teacher_list')

# -------------------------------
# Course CRUD
# -------------------------------
@login_required
@role_required('admin')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'admin_app/course_list.html', {'courses': courses})

@login_required
@role_required('admin')
def add_course(request):
    form = AddCourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Course added successfully!')
        return redirect('course_list')
    return render(request, 'admin_app/add_course.html', {'form': form})

@login_required
@role_required('admin')
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = AddCourseForm(request.POST or None, instance=course)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('course_list')

    return render(request, 'admin_app/edit_course.html', {'form': form})

@login_required
@role_required('admin')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('course_list')

# -------------------------------
# Predictive Analytics Views
# -------------------------------
@login_required
@role_required('admin')
def predictive_analytics(request):
    """Predictive Analytics Dashboard"""
    from .predictive_analytics import predictor
    
    students = Student.objects.all()
    predictions = []
    
    for student in students:
        prediction = predictor.predict_performance(student)
        predictions.append({
            'student': student,
            'prediction': prediction
        })
    
    # Sort by risk level
    predictions.sort(key=lambda x: x['prediction']['predicted_marks'])
    
    # Count risk levels
    high_risk_count = sum(1 for p in predictions if p['prediction']['risk_level'] == 'High Risk')
    medium_risk_count = sum(1 for p in predictions if p['prediction']['risk_level'] == 'Medium Risk')
    low_risk_count = sum(1 for p in predictions if p['prediction']['risk_level'] == 'Low Risk')
    
    context = {
        'predictions': predictions,
        'total_students': len(predictions),
        'high_risk_count': high_risk_count,
        'medium_risk_count': medium_risk_count,
        'low_risk_count': low_risk_count
    }
    return render(request, 'admin_app/predictive_analytics.html', context)

# at_risk_students view removed - functionality moved to predictive_analytics

# -------------------------------
# Analytics View
# -------------------------------
@login_required
@role_required('admin')
def admin_analytics(request):
    # Import seaborn visualizer
    from .seaborn_charts import visualizer
    from teacher_app.models import Attendance, StudentMarks
    
    # Get statistics for dashboard
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    
    # Attendance statistics
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='Present').count()
    absent_count = total_attendance - present_count
    
    attendance_percentage = 0
    if total_attendance > 0:
        attendance_percentage = (present_count / total_attendance) * 100
    
    # Course distribution
    course_distribution = []
    for course in Course.objects.all():
        student_count = Student.objects.filter(course=course).count()
        course_distribution.append({
            'name': course.name,
            'count': student_count
        })
    
    # Teacher-student ratio by course
    teacher_student_ratio = []
    for course in Course.objects.all():
        teacher_count = course.teachers.count()
        student_count = Student.objects.filter(course=course).count()
        
        ratio = 0
        if teacher_count > 0:
            ratio = student_count / teacher_count
        
        teacher_student_ratio.append({
            'course': course.name,
            'ratio': round(ratio, 1)
        })
    
    # Performance by course
    performance_by_course = []
    for course in Course.objects.all():
        marks = StudentMarks.objects.filter(course=course)
        avg_marks = 0
        
        if marks.exists():
            total_percentage = 0
            for mark in marks:
                percentage = (mark.marks / mark.max_marks) * 100
                total_percentage += percentage
            
            avg_marks = total_percentage / marks.count()
        
        performance_by_course.append({
            'course': course.name,
            'avg_marks': round(avg_marks, 1)
        })
    
    # Generate seaborn charts
    attendance_chart = visualizer.attendance_pie_chart()
    course_chart = visualizer.course_distribution_bar()
    performance_chart = visualizer.performance_heatmap()
    risk_chart = visualizer.risk_level_chart()
    
    return render(request, 'admin_app/analytics_seaborn.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'attendance_percentage': round(attendance_percentage, 1),
        'attendance_chart': attendance_chart,
        'course_chart': course_chart,
        'performance_chart': performance_chart,
        'risk_chart': risk_chart,
    })

# -------------------------------
# List Views
# -------------------------------
@login_required
@role_required('admin')
def student_list(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        students = students.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(student_id__icontains=search)
        )
    
    # Filter by course
    course_filter = request.GET.get('course')
    if course_filter:
        students = students.filter(course_id=course_filter)
    
    # Filter by timing
    timing_filter = request.GET.get('timing')
    if timing_filter:
        students = students.filter(timing=timing_filter)
    
    return render(request, 'admin_app/student_list.html', {
        'students': students,
        'courses': courses
    })

@login_required
@role_required('admin')
def teacher_list(request):
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        teachers = teachers.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(teacher_id__icontains=search)
        )
    
    # Filter by course
    course_filter = request.GET.get('course')
    if course_filter:
        teachers = teachers.filter(courses__id=course_filter)
    
    # Filter by timing
    timing_filter = request.GET.get('timing')
    if timing_filter:
        teachers = teachers.filter(timing__icontains=timing_filter)
    
    return render(request, 'admin_app/teacher_list.html', {
        'teachers': teachers,
        'courses': courses
    })
