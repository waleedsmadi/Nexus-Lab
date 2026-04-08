from django import forms
from .models import Submission
import magic
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['id', 'user', 'status', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'vdp-title',
                'maxlength': 250,
                'placeholder': 'Title...',
            }),


            'vulner_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'vdp-vulner_type',
            }),

            'severity': forms.Select(attrs={
                'class': 'form-select',
                'id': 'vdp-severity',
            }),

            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'id': 'vdp-url',
                'placeholder': 'https://nexus.com/ ...',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vdp-description',
                'placeholder': 'Explain the vulnerability ...',
                'style': 'resize: none;',
                'rows': '15',
                'cols': '5',
            }),


            'steps_to_reproduce': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vdp-steps_to_reproduce',
                'placeholder': 'Explain How do I reach the vulnerability step by step ...',
                'style': 'resize: none;',
                'rows': '15',
                'cols': '5',
            }),


            'poc': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'vdp-poc',
            }),


            'impact': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vdp-impact',
                'placeholder': 'Explain the worst-case scenario that could happen ...',
                'style': 'resize: none;',
                'rows': '5',
                'cols': '5',
            }),

            'recommended_fix': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'vdp-recommended_fix',
                'placeholder': 'Suggest a solution to the problem ...',
                'style': 'resize: none;',
                'rows': '6',
                'cols': '5',
            }),
        }



    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "recommended_fix":
                field.required = False
            else:
                field.required = True
            field.help_text = ''
            field.label = ''

    def clean_poc(self):
        poc = self.cleaned_data.get('poc')
        if not poc:
            return poc
        
        file_head = poc.read(2048)
        mime = magic.from_buffer(file_head, mime=True)
        poc.seek(0)
        if mime not in ["image/png", "image/jpeg", "video/mp4", 'video/quicktime']:
            raise ValidationError(f"Error: File type '{mime}' is not allowed.!")
            
        return poc

    

    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url:
            return url
        parsed = urlparse(url)


        if not parsed.scheme or not parsed.netloc:
            raise ValidationError('Error: Invalid url.!')
        
        if parsed.netloc != self.request.get_host():
            raise ValidationError('Error: URL must belong to Nexus Lab.!')
        
        return url




    


    
            

