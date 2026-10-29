from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from marketplace.views import show_market, contact, detail, new, delete, edit, new_conversation

app_name = 'marketplace'

urlpatterns = [
    path('', show_market, name="show_market"),
    path('contact/', contact, name="contact"),
    path('new/', new, name="new"),  # Rute spesifik harus di atas <int:pk>
    path('<int:pk>/', detail, name="detail"),
    path('<int:pk>/delete/', delete, name="delete"),
    path('<int:pk>/edit/', edit, name="edit"),  # Rute edit spesifik dengan akhiran /edit/
    path('<int:item_pk>/conversation/', new_conversation, name="new_conversation"),
    ]