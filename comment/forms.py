from django import forms
from .models import Comment
from django.core.exceptions import ValidationError



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text',]
        help_texts = {'text': ''}
        labels = {'text': ''}
        max_length = 500
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment-textarea',
                'placeholder': 'Write a comment here',
                'style': 'height: 100px; border: 1px solid blue; resize: none;',
                'maxlength': '500',
                "onkeydown": 'preventEnter(this, event)',
                "onkeyup": "disableBtnWhenTextEmpty(this, this.parentElement.nextElementSibling, event)",
            })
        }

        

    

    def clean_text(self):
        text = self.cleaned_data.get('text')

        if not text:
            raise ValidationError('Error: The comment must not be empty!')
        return text
    


class EditCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text',]
        help_texts = {'text': ''}
        labels = {'text': ''}
        max_length = 500
        widgets = {
            'text': forms.Textarea(attrs={
                'class': "edit-comment-text ms-2  bg-white border rounded shadow-sm flex-grow-1",
                'id': "edit-comment-text-{{comment.pk}}",
                'placeholder': 'Write a comment here',
                'style': "outline: 1px solid blue; max-width: 700px; word-wrap: break-word; resize: none;",
                'maxlength': '500',
                "onkeydown": "handleEnterForm(this, event)",
                "onkeyup": "disableBtnWhenTextEmpty(this, this.previousElementSibling, event)",
                'rows': "4",
                "autofocus": "true",

            })
        }

    

    def clean_text(self):
        text = self.cleaned_data.get('text')

        if not text:
            raise ValidationError('Error: The comment must not be empty!')
        return text