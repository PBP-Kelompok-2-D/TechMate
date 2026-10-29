import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.URLField(blank=True,null=True)
    bio = models.TextField(max_length=256, blank=True)