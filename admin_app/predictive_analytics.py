from django.db.models import Avg, Count
from datetime import datetime, timedelta
from student_app.models import Student
from teacher_app.models import StudentMarks, Attendance

class PredictiveAnalytics:
    def predict_performance(self, student):
        """Predict student performance based on attendance and marks"""
        attendance_records = Attendance.objects.filter(student=student)
        marks_records = StudentMarks.objects.filter(student=student)
        
        if not attendance_records.exists():
            attendance_rate = 85.0
        else:
            total_days = attendance_records.count()
            present_days = attendance_records.filter(status='Present').count()
            attendance_rate = (present_days / total_days) * 100
        
        # Get recent trend (last 30 days)
        recent_date = datetime.now().date() - timedelta(days=30)
        recent_attendance = attendance_records.filter(date__gte=recent_date)
        
        if recent_attendance.exists():
            recent_present = recent_attendance.filter(status='Present').count()
            recent_rate = (recent_present / recent_attendance.count()) * 100
            trend = recent_rate - attendance_rate
        else:
            trend = 0
        
        # Calculate consecutive absences
        consecutive_absences = 0
        for record in attendance_records.order_by('-date')[:10]:
            if record.status == 'Absent':
                consecutive_absences += 1
            else:
                break
        
        # Get current average marks (percentage)
        if marks_records.exists():
            total_marks = 0
            total_max_marks = 0
            for mark in marks_records:
                total_marks += mark.marks
                total_max_marks += mark.max_marks
            current_avg = (total_marks / total_max_marks) * 100 if total_max_marks > 0 else 0
        else:
            current_avg = 0
        
        # Prediction algorithm - Simple formula
        # Base prediction on attendance (60%) + current performance (40%)
        attendance_factor = attendance_rate * 0.6
        performance_factor = current_avg * 0.4 if current_avg > 0 else attendance_rate * 0.4
        
        predicted_marks = attendance_factor + performance_factor
        
        # Apply trend adjustment
        if trend < -10:  # Declining trend
            predicted_marks -= 10
        elif trend > 10:  # Improving trend
            predicted_marks += 5
        
        # Penalty for consecutive absences
        if consecutive_absences >= 3:
            predicted_marks -= (consecutive_absences * 3)
        
        predicted_marks = max(0, min(100, predicted_marks))
        
        # Risk assessment
        if predicted_marks < 40:
            risk_level = "High Risk"
            risk_color = "danger"
        elif predicted_marks < 60:
            risk_level = "Medium Risk"
            risk_color = "warning"
        else:
            risk_level = "Low Risk"
            risk_color = "success"
        
        return {
            'predicted_marks': round(predicted_marks, 2),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'attendance_rate': round(attendance_rate, 2),
            'trend': round(trend, 2),
            'consecutive_absences': consecutive_absences,
            'current_avg': round(current_avg, 2) if current_avg else 0
        }
    
    def get_at_risk_students(self):
        """Get list of at-risk students"""
        at_risk_students = []
        
        for student in Student.objects.all():
            prediction = self.predict_performance(student)
            
            # Multiple risk criteria
            is_at_risk = (
                prediction['predicted_marks'] < 50 or
                prediction['attendance_rate'] < 70 or
                prediction['consecutive_absences'] >= 3 or
                prediction['trend'] < -15
            )
            
            if is_at_risk:
                recommendations = self.get_recommendations(prediction)
                priority = self.calculate_priority(prediction)
                
                at_risk_students.append({
                    'student': student,
                    'prediction': prediction,
                    'recommendations': recommendations,
                    'priority': priority
                })
        
        # Sort by priority
        at_risk_students.sort(key=lambda x: x['priority'], reverse=True)
        return at_risk_students
    
    def get_recommendations(self, prediction):
        """Generate ML-based recommendations"""
        recommendations = []
        
        if prediction['attendance_rate'] < 70:
            recommendations.append("📞 Contact parents immediately")
            recommendations.append("📋 Daily attendance monitoring")
        
        if prediction['consecutive_absences'] >= 3:
            recommendations.append("🚨 Emergency intervention needed")
            recommendations.append("🏥 Check health/personal issues")
        
        if prediction['trend'] < -10:
            recommendations.append("📉 Address declining pattern")
            recommendations.append("🤝 Counseling session required")
        
        if prediction['predicted_marks'] < 40:
            recommendations.append("📚 Intensive tutoring program")
            recommendations.append("📝 Extra assignments and practice")
        
        if prediction['current_avg'] < 50 and prediction['current_avg'] > 0:
            recommendations.append("🎯 Subject-specific help needed")
            recommendations.append("👥 Peer study groups")
        
        return recommendations
    
    def calculate_priority(self, prediction):
        """Calculate intervention priority (0-100)"""
        priority = 0
        
        # Attendance priority
        if prediction['attendance_rate'] < 50:
            priority += 40
        elif prediction['attendance_rate'] < 70:
            priority += 25
        
        # Performance priority
        if prediction['predicted_marks'] < 30:
            priority += 35
        elif prediction['predicted_marks'] < 50:
            priority += 20
        
        # Trend priority
        if prediction['trend'] < -20:
            priority += 20
        elif prediction['trend'] < -10:
            priority += 10
        
        # Consecutive absence penalty
        priority += min(prediction['consecutive_absences'] * 3, 15)
        
        return min(100, priority)

predictor = PredictiveAnalytics()