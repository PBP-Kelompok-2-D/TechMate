from django import forms
from .models import Comment
# from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content','parent']
        
        labels = {
            'content': 'Content',
        }
        
        widgets = {
            'content' : forms.TextInput(
                attrs={
                    'placeholder': "Komentar",
                }
            ),
        }