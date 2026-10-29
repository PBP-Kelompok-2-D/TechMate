from django import forms

from marketplace.models import Item, ConversationMessage

INPUT_CLASS = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'image', 'contact_number',]

        widgets = {
            'category' : forms.Select(attrs={
                'class': INPUT_CLASS
            }),
            'name' : forms.TextInput(attrs={
                'class': INPUT_CLASS
            }),
            'description' : forms.Textarea(attrs={
                'class': INPUT_CLASS
            }),
            'price' : forms.TextInput(attrs={
                            'class': INPUT_CLASS
            }),
            'image' : forms.FileInput(attrs={
                            'class': INPUT_CLASS
            }),
            'contact_number': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Nomor WhatsApp (contoh: 6285817544682) atau Link IG'
            }),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'is_sold']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class': INPUT_CLASS
            }),
            'description' : forms.Textarea(attrs={
                'class': INPUT_CLASS
            }),
            'price' : forms.TextInput(attrs={
                            'class': INPUT_CLASS
            }),
            'image' : forms.FileInput(attrs={
                            'class': INPUT_CLASS
            })
        }

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content',]
        widgets = {
            'content' : forms.Textarea(attrs={
                'class' : 'w-full py-4 px-6 rounded-xl border'
            })
        }
