# admin.py — Makes the Laptop model visible and editable in Django's admin
# panel at /admin, which is handy for checking what the API saved.

from django.contrib import admin

from .models import Laptop

admin.site.register(Laptop)
