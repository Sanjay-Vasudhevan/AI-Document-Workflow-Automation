from django import forms
from .models import Document
import os

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter document title'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = os.path.splitext(file.name)[1].lower()
            valid_extensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
            if ext not in valid_extensions:
                raise forms.ValidationError("Unsupported file format! Please upload a PDF, DOCX, or Image.")
        return file