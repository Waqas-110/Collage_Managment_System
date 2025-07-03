# admin_app/chart_generator.py
# Chart generation using Seaborn for Django admin dashboard
import matplotlib # Use a non-GUI backend for matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt # Import matplotlib for plotting
import seaborn as sns # Import seaborn for advanced plotting
import pandas as pd # Import pandas for data manipulation
import io # Import io for handling byte streams
import base64 # Import base64 for encoding images
from django.db.models import Count, Avg # Import Django ORM functions for aggregation
from student_app.models import Student # Import Student model from student_app
from teacher_app.models import Attendance, StudentMarks # Import Attendance and StudentMarks models from teacher_app

class SeabornCharts:
    def __init__(self):
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8') # Set Seaborn style for plots
    
    def generate_attendance_chart(self):
        """Generate attendance distribution chart"""
        attendance_data = Attendance.objects.values('status').annotate(count=Count('status')) 
        
        if not attendance_data:
            return None
        
        df = pd.DataFrame(attendance_data)
        
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x='status', palette='viridis')
        plt.title('Attendance Distribution')
        plt.xlabel('Status')
        plt.ylabel('Count')
        
        return self._get_image_base64() 
    
    def generate_performance_chart(self):
        """Generate performance by course chart"""
        marks_data = StudentMarks.objects.select_related('course').values('course__name').annotate(avg_marks=Avg('marks'))
        
        if not marks_data:
            return None
        
        df = pd.DataFrame(marks_data)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='course__name', y='avg_marks', palette='coolwarm')
        plt.title('Average Performance by Course')
        plt.xlabel('Course')
        plt.ylabel('Average Marks')
        plt.xticks(rotation=45)
        
        return self._get_image_base64()
    
    def _get_image_base64(self):
        """Convert plot to base64 string"""
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return f"data:image/png;base64,{image_base64}"

chart_generator = SeabornCharts()