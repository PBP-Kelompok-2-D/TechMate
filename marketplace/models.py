from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    CATEGORY_CHOICES = [
        ("smartphone", "Smartphone"),
        ("laptop", "Laptop"),
        ("tablet", "Tablet"),
    ]
    name = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default= "smartphone",)

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    CATEGORY_CHOICES = [
        ("smartphone", "Smartphone"),
        ("laptop", "Laptop"),
        ("tablet", "Tablet"),
    ]

    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default= "smartphone",)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    image = models.URLField( blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True, help_text="Nomor WhatsApp (misal: 6281234567890) atau Username/Link Kontak")
    created_by = models.ForeignKey(User, related_name='items', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)