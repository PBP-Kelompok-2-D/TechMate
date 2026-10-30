from django.forms import ModelForm, TextInput, Textarea, URLInput
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from .models import Profile, Report

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar",
                "bio"]
        labels = {
            "avatar": "URL Foto / Avatar",
            "bio": "Bio Profil",
        }
        widgets = {
            "avatar": URLInput(
                attrs={
                    "placeholder": "https://... (link foto luar)"
                }
            ),
            "bio": Textarea(
                attrs={
                    "placeholder": "Tulis bio singkat...",
                    "rows": 3
                }
            ),
        }

    def clean_bio(self):
        return strip_tags(self.cleaned_data["bio"]).strip()
    
class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["description"]
        labels = {
            "description": "Alasan Laporan",
        }
        widgets = {
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan alasan Anda melaporkan pengguna ini...",
                    "rows": 4
                }
            ),
        }

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi laporan tidak boleh kosong.")
        return description