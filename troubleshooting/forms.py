from django import forms
from .models import ArticleFeedback

class ArticleFeedbackForm(forms.ModelForm):
    class Meta:
        model = ArticleFeedback
        fields = ['is_solved', 'actual_repair_cost', 'comment']
        widgets = {
            'is_solved': forms.Select(
                choices=[(True, 'Ya, berhasil teratasi'), (False, 'Belum berhasil / Butuh ke teknisi')],
                attrs={'class': 'w-full rounded-lg border-gray-300 p-2.5 text-sm'}
            ),
            'actual_repair_cost': forms.NumberInput(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2.5 text-sm',
                    'placeholder': 'Contoh: 150000 (Kosongkan jika gratis/DIY)',
                    'min': '0'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'w-full rounded-lg border-gray-300 p-2.5 text-sm',
                    'rows': 3,
                    'placeholder': 'Bagikan tips tambahan, lokasi servis, atau pengalamanmu memperbaiki masalah ini...'
                }
            ),
        }