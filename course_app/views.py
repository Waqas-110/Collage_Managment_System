from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Course

@login_required
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'course_app/manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            if not name:
                messages.error(request, "Course name is required")
                return redirect('course_app:add_course')

            Course.objects.create(name=name)
            messages.success(request, "Course added successfully")
            return redirect('course_app:manage_courses')
        except Exception as e:
            messages.error(request, f"Error adding course: {str(e)}")
            return redirect('course_app:add_course')

    return render(request, 'course_app/add_course.html')

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            course.name = name
            course.save()
            messages.success(request, "Course updated successfully!")
            return redirect('course_app:manage_courses')
        messages.error(request, "Course name is required")
    return render(request, 'course_app/edit_course.html', {'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('course_app:manage_courses')