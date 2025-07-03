from django.shortcuts import render, redirect, get_object_or_404
from student_app.models import Student
from course_app.models import Course
from teacher_app.models import Teacher, Attendance, StudentMarks
from .forms import AttendanceForm
from admin_app.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

@login_required
@role_required('teacher')
def teacher_home(request):
    try:
        teacher = request.user.teacher
        courses = teacher.courses.all()
        
        # Calculate total students under this teacher
        total_students = 0
        for course in courses:
            total_students += course.student_set.count()
        
        context = {
            'teacher': teacher,
            'courses': courses,
            'total_students': total_students
        }
    except:
        context = {}
    
    return render(request, 'teacher_app/teacher_home.html', context)

@login_required
@role_required('teacher')
def mark_attendance(request):
    teacher = request.user.teacher
    today = datetime.date.today()

    # Get students in teacher's courses - using the many-to-many relationship
    teacher_courses = teacher.courses.all()
    students = Student.objects.filter(course__in=teacher_courses)

    if request.method == 'POST':
        # Process the form submission directly
        for student in students:
            status = request.POST.get(f'student_{student.id}')
            if status:  # Only create attendance if status was submitted
                Attendance.objects.create(
                    student=student,
                    teacher=teacher,
                    course=student.course,
                    date=today,
                    status=status
                )
        return redirect('teacher_home')

    return render(request, 'teacher_app/mark_attendance.html', {
        'students': students,
        'today': today,
    })

@login_required
@role_required('teacher')
def view_attendance(request):
    teacher = request.user.teacher
    
    # Get date filter
    date_filter = request.GET.get('date')
    course_filter = request.GET.get('course')
    
    # Base query
    attendance_records = Attendance.objects.filter(teacher=teacher)
    
    # Apply filters
    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)
    
    if course_filter:
        attendance_records = attendance_records.filter(course_id=course_filter)
    
    # Get courses for filter dropdown
    courses = teacher.courses.all()
    
    return render(request, 'teacher_app/view_attendance.html', {
        'attendance_records': attendance_records,
        'courses': courses,
        'selected_date': date_filter,
        'selected_course': course_filter,
    })

@login_required
@role_required('teacher')
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id, teacher=request.user.teacher)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['Present', 'Absent']:
            attendance.status = status
            attendance.save()
            messages.success(request, 'Attendance updated successfully!')
            return redirect('view_attendance')
    
    return render(request, 'teacher_app/edit_attendance.html', {
        'attendance': attendance,
    })

@login_required
@role_required('teacher')
def give_marks(request):
    teacher = request.user.teacher
    today = datetime.date.today()
    
    # Get students in teacher's courses
    teacher_courses = teacher.courses.all()
    students = Student.objects.filter(course__in=teacher_courses)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        marks_for = request.POST.get('marks_for')
        marks = request.POST.get('marks')
        max_marks = request.POST.get('max_marks', 100)
        exam_date = request.POST.get('exam_date', today.strftime('%Y-%m-%d'))
        remarks = request.POST.get('remarks', '')
        
        if student_id and course_id and marks and marks_for:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            
            # Create or update marks
            StudentMarks.objects.create(
                student=student,
                teacher=teacher,
                course=course,
                marks_for=marks_for,
                marks=marks,
                max_marks=max_marks,
                exam_date=exam_date,
                remarks=remarks
            )
            
            return redirect('give_marks')
    
    # Get existing marks
    student_marks = StudentMarks.objects.filter(teacher=teacher)
    
    return render(request, 'teacher_app/give_marks.html', {
        'teacher': teacher,
        'students': students,
        'courses': teacher_courses,
        'student_marks': student_marks,
        'today': today
    })

@login_required
@role_required('teacher')
def view_marks(request):
    teacher = request.user.teacher
    
    # Get filters
    course_filter = request.GET.get('course')
    exam_type_filter = request.GET.get('exam_type')
    
    # Base query
    marks_records = StudentMarks.objects.filter(teacher=teacher)
    
    # Apply filters
    if course_filter:
        marks_records = marks_records.filter(course_id=course_filter)
    
    if exam_type_filter:
        marks_records = marks_records.filter(marks_for=exam_type_filter)
    
    # Get courses for filter dropdown
    courses = teacher.courses.all()
    
    # Get exam types for filter dropdown
    exam_types = StudentMarks.MARKS_TYPE_CHOICES
    
    return render(request, 'teacher_app/view_marks.html', {
        'marks_records': marks_records,
        'courses': courses,
        'exam_types': exam_types,
        'selected_course': course_filter,
        'selected_exam_type': exam_type_filter,
    })

@login_required
@role_required('teacher')
def edit_marks(request, marks_id):
    marks = get_object_or_404(StudentMarks, id=marks_id, teacher=request.user.teacher)
    
    if request.method == 'POST':
        marks_value = request.POST.get('marks')
        max_marks = request.POST.get('max_marks')
        remarks = request.POST.get('remarks', '')
        
        if marks_value and max_marks:
            marks.marks = marks_value
            marks.max_marks = max_marks
            marks.remarks = remarks
            marks.save()
            messages.success(request, 'Marks updated successfully!')
            return redirect('view_marks')
    
    return render(request, 'teacher_app/edit_marks.html', {
        'marks': marks,
    })