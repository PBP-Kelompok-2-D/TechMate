from django import forms
from .models import Blog, Comment, Review

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Thread/Pertanyaan'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deskripsi Singkat'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tulis isi diskusi atau pertanyaanmu secara detail...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tulis balasan atau komentarmu di sini...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['device_name', 'rating', 'review_text'] # is_durable dihapus dari fields
        labels = {
            'device_name': 'Nama Perangkat',
            'rating': 'Rating',
            'review_text': 'Ulasan'
        }
        widgets = {
            'device_name': forms.TextInput(attrs={'placeholder': 'Contoh: Samsung Galaxy S22'}),
            'rating': forms.Select(),
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ceritakan pengalamanmu menggunakan perangkat ini...'}),
        }