from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        
        labels = {
            'content': 'Content',
        }
        
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Tulis komentar...',
                    'rows': 4,
                }
            ),
        }