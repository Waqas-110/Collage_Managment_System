from django import forms
from .models import Course

class AddCourseForm(forms.ModelForm):
    TIMING_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    
    timing = forms.MultipleChoiceField(
        choices=TIMING_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Course Name',
            'code': 'Course Code',
            'description': 'Course Description',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing course, split the timing string into a list
        if self.instance.pk and self.instance.timing:
            self.initial['timing'] = self.instance.timing.split(',')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Join the selected timing values with commas
        instance.timing = ','.join(self.cleaned_data.get('timing', []))
        
        if commit:
            instance.save()
        
        return instance