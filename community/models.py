from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# 1. MODEL UNTUK THREAD FORUM DISKUSI
class Blog(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    description = models.CharField(max_length=355, null=True)
    content = models.TextField()
    published_date_time = models.DateTimeField(default=timezone.now)
    upvoted_by = models.ManyToManyField(User, related_name="upvotes", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
# 2. MODEL UNTUK KOMENTAR BALASAN
class Comment(models.Model):
    CommentPost = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.author} comment: {self.content}"

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        return self.parent is None

# 3. MODEL UNTUK RATING & REVIEW GADGET
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Sangat Buruk'),
        (2, '2 - Buruk'),
        (3, '3 - Cukup'),
        (4, '4 - Bagus'),
        (5, '5 - Sangat Bagus'),
    ]
    
    device_name = models.CharField(max_length=255) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    # Fitur wajib untuk mengecek durabilitas:
    is_durable = models.BooleanField(default=True, verbose_name="Apakah awet dipakai > 2 tahun?") 
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.device_name} by {self.author.username}"