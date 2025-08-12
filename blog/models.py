from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Post model
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('travel', 'Travel'),
        ('lifestyle', 'Lifestyle'),
        ('news', 'News'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # CKEditor with image upload
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other') 
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User


