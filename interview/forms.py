from django.forms import ModelForm
from .models import Application

class ApplicationUploadForm(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
