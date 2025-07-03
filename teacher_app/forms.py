from django import forms
from .models import Teacher
from django.contrib.auth.models import User
from course_app.models import Course

class AddTeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    teacher_id = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        required=False
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    timing = forms.MultipleChoiceField(
        choices=[
            ('Morning', 'Morning'),
            ('Afternoon', 'Afternoon'),
            ('Evening', 'Evening'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'age', 'email', 'courses', 'timing', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        timing_list = self.cleaned_data.get('timing', [])
        instance.timing = ','.join(timing_list)
        
        if commit:
            instance.save()
            self.save_m2m()  # Save many-to-many relationships
        
        return instance

class AttendanceForm(forms.Form):
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            for student in students:
                self.fields[f'student_{student.id}'] = forms.ChoiceField(
                    label=f"{student.first_name} {student.last_name}",
                    choices=[('Present', 'Present'), ('Absent', 'Absent')],
                    widget=forms.RadioSelect
                )