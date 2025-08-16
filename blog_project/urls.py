# blog_project/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from blog import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication

    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register_view, name='register'),
     
    # Main Pages
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('create_post/', views.create_post, name='create_post'),
    path('show_blog/', views.show_blog, name='show_blog'),
    path('about/', views.about, name='about'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('post/<int:id>/edit/', views.edit_blog, name='edit_blog'),
    path('post/<int:id>/delete/', views.delete_blog, name='delete_blog'),

    # Category-based Filter
    path('category/<str:category>/', views.home, name='category_filter'),

    # CKEditor Uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


# Media Files in Development Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)