from django.shortcuts import render

def course_home(request):
    return render(request, 'course_app/course_home.html')
