from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from marketplace.views import index, contact, detail, new, delete, edit, new_conversation

app_name = 'marketplace'

urlpatterns = [
    path('', index, name="index"),
    path('contact/', contact, name="contact"),
    path('<int:pk>/', detail, name="detail" ),
    path('<int:pk>/delete/', delete, name="delete" ),
    path('<int:pk>/edit/', edit, name="edit" ),
    path('new/', new, name="new"),
    path('<int:pk>/', new_conversation, name="new_conversation" ),
]