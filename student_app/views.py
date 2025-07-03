from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admin_app.decorators import role_required
from teacher_app.models import Attendance, StudentMarks
from django.db.models import Count, Avg
import json

@login_required
@role_required('student')
def student_home(request):
    try:
        student = request.user.student
        
        # Get attendance statistics
        total_classes = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(student=student, status='Present').count()
        absent_count = total_classes - present_count
        
        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = (present_count / total_classes) * 100
        
        # Get marks statistics
        marks_records = StudentMarks.objects.filter(student=student)
        total_exams = marks_records.count()
        
        avg_marks = 0
        if total_exams > 0:
            avg_marks = marks_records.aggregate(Avg('marks'))['marks__avg']
        
        # Predicted performance using admin's predictor
        from admin_app.predictive_analytics import predictor
        prediction = predictor.predict_performance(student)
        
        # Get teacher remarks (latest 3)
        teacher_remarks = marks_records.exclude(remarks__isnull=True).exclude(remarks='').order_by('-exam_date')[:3]
        
        # Attendance chart data (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_attendance = Attendance.objects.filter(student=student, date__gte=thirty_days_ago).order_by('date')
        
        chart_data = []
        for record in recent_attendance:
            chart_data.append({
                'date': record.date.strftime('%m/%d'),
                'status': 1 if record.status == 'Present' else 0
            })
        
        # Check for warnings
        warning_message = None
        if attendance_percentage < 70:
            warning_message = f"⚠️ Warning: Your attendance is {attendance_percentage:.1f}%. Please improve to avoid academic issues."
        elif avg_marks and avg_marks < 50:
            warning_message = f"⚠️ Warning: Your average marks are {avg_marks:.1f}%. Extra study required."
        
        context = {
            'student': student,
            'total_classes': total_classes,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_percentage': round(attendance_percentage, 1),
            'total_exams': total_exams,
            'avg_marks': round(avg_marks, 1) if avg_marks else 0,
            'warning_message': warning_message,
            'prediction': prediction,
            'teacher_remarks': teacher_remarks,
            'chart_data': json.dumps(chart_data),
        }
    except:
        context = {}
    
    return render(request, 'student_app/student_home.html', context)

@login_required
@role_required('student')
def view_attendance(request):
    student = request.user.student
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    
    # Calculate attendance statistics
    total_classes = attendance_records.count()
    present_count = attendance_records.filter(status='Present').count()
    absent_count = total_classes - present_count
    
    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = (present_count / total_classes) * 100
    
    # Prepare data for chart
    attendance_by_month = {}
    for record in attendance_records:
        month_key = record.date.strftime('%b %Y')
        if month_key not in attendance_by_month:
            attendance_by_month[month_key] = {'present': 0, 'absent': 0}
        
        if record.status == 'Present':
            attendance_by_month[month_key]['present'] += 1
        else:
            attendance_by_month[month_key]['absent'] += 1
    
    # Convert to format for chart.js
    chart_labels = list(attendance_by_month.keys())
    chart_present_data = [attendance_by_month[month]['present'] for month in chart_labels]
    chart_absent_data = [attendance_by_month[month]['absent'] for month in chart_labels]
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'chart_labels': json.dumps(chart_labels),
        'chart_present_data': json.dumps(chart_present_data),
        'chart_absent_data': json.dumps(chart_absent_data),
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': round(attendance_percentage, 1),
    }
    
    return render(request, 'student_app/view_attendance.html', context)

@login_required
@role_required('student')
def view_marks(request):
    student = request.user.student
    
    # Get marks records
    marks_records = StudentMarks.objects.filter(student=student).order_by('-exam_date')
    
    # Prepare data for chart
    marks_by_type = {}
    for record in marks_records:
        if record.marks_for not in marks_by_type:
            marks_by_type[record.marks_for] = []
        
        percentage = (record.marks / record.max_marks) * 100
        marks_by_type[record.marks_for].append(percentage)
    
    # Calculate average for each type
    chart_labels = list(marks_by_type.keys())
    chart_data = []
    
    for exam_type in chart_labels:
        avg = sum(marks_by_type[exam_type]) / len(marks_by_type[exam_type])
        chart_data.append(round(avg, 1))
    
    context = {
        'student': student,
        'marks_records': marks_records,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'student_app/view_marks.html', context)