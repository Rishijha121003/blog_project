"""
WSGI config for blog_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

application = get_wsgi_application()
from django.contrib.sessions.models import Session

try:
    Session.objects.all().delete()
    print("All old sessions cleared from WSGI!")
except Exception as e:
    print("Session clear failed:", e)