from django.contrib import admin
from .models import Post  # ya jo bhi model hai
from .models import Blog, Category
admin.site.register(Post)
# blog/admin.py


admin.site.register(Blog)
admin.site.register(Category)
