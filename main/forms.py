from django.forms import ModelForm, TextInput, Textarea, URLInput
from .models import Profile

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