from django.apps import AppConfig
from django.core.cache import cache
cache.clear()


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'