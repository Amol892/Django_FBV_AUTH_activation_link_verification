from django import forms 
from .models import Project_details

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project_details
        fields = '__all__'