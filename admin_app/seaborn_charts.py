import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from django.db.models import Count, Avg
from student_app.models import Student
from teacher_app.models import Attendance, StudentMarks
from course_app.models import Course

class SeabornVisualizer:
    def __init__(self):
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'
    
    def attendance_pie_chart(self):
        """Attendance distribution pie chart"""
        present = Attendance.objects.filter(status='Present').count()
        absent = Attendance.objects.filter(status='Absent').count()
        
        if present == 0 and absent == 0:
            present, absent = 80, 20  # Default data
        
        plt.figure(figsize=(8, 6))
        plt.pie([present, absent], labels=['Present', 'Absent'], 
                autopct='%1.1f%%', colors=['#28a745', '#dc3545'])
        plt.title('Attendance Distribution', fontsize=16, fontweight='bold')
        return self._to_base64()
    
    def course_distribution_bar(self):
        """Students per course bar chart"""
        courses = Course.objects.all()
        course_data = []
        
        for course in courses:
            count = Student.objects.filter(course=course).count()
            course_data.append({'Course': course.name, 'Students': count})
        
        if not course_data:
            course_data = [{'Course': 'No Data', 'Students': 0}]
        
        df = pd.DataFrame(course_data)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='Course', y='Students', palette='viridis')
        plt.title('Students Distribution by Course', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return self._to_base64()
    
    def performance_heatmap(self):
        """Performance heatmap by course"""
        marks_data = []
        courses = Course.objects.all()
        
        for course in courses:
            marks = StudentMarks.objects.filter(course=course)
            if marks.exists():
                avg_marks = marks.aggregate(avg=Avg('marks'))['avg']
                marks_data.append({
                    'Course': course.name,
                    'Average': round(avg_marks, 1)
                })
        
        if not marks_data:
            marks_data = [{'Course': 'No Data', 'Average': 0}]
        
        df = pd.DataFrame(marks_data)
        pivot_df = df.set_index('Course').T
        
        plt.figure(figsize=(10, 4))
        sns.heatmap(pivot_df, annot=True, cmap='RdYlGn', center=50, 
                   cbar_kws={'label': 'Average Marks'})
        plt.title('Performance Heatmap by Course', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return self._to_base64()
    
    def risk_level_chart(self):
        """At-risk students visualization"""
        from .predictive_analytics import predictor
        
        risk_data = {'High Risk': 0, 'Medium Risk': 0, 'Low Risk': 0}
        
        for student in Student.objects.all():
            prediction = predictor.predict_performance(student)
            risk_data[prediction['risk_level']] += 1
        
        plt.figure(figsize=(8, 6))
        colors = ['#dc3545', '#ffc107', '#28a745']
        plt.bar(risk_data.keys(), risk_data.values(), color=colors)
        plt.title('Student Risk Level Distribution', fontsize=16, fontweight='bold')
        plt.ylabel('Number of Students')
        return self._to_base64()
    
    def _to_base64(self):
        """Convert plot to base64 string"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{image_base64}"

visualizer = SeabornVisualizer()