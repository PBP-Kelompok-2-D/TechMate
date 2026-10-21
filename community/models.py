from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Blog(models.Model):
    slug = models.SlugField(max_length=255, unique=True) #id untuk blog
    title = models.CharField(max_length=255 , unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts')
    description = models.CharField(max_length=355, null=True)
    content = models.TextField()
    published_date_time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    CommentPost = models.ForeignKey(Blog , on_delete=models.CASCADE)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self): #reply
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False