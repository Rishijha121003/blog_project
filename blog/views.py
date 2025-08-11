from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post, Blog, Category
from collections import defaultdict
from .models import BlogPost
from django.utils import timezone
def base(request):
    return render(request, 'blog/base.html')  






@login_required
def home(request):
    latest_blogs = BlogPost.objects.order_by('-created_at')[:6]  # Latest 6 blogs
    return render(request, 'blog/home.html', {'latest_blogs': latest_blogs})

   
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # ya jahan redirect karna ho
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})





# views.py
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # ya jahan redirect karna ho
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'blog/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('login')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'blog/register.html')
def custom_logout(request):
    logout(request)
    return redirect('login')
def show_blog(request):
    selected_categories = request.GET.getlist('category')  # e.g. ['tech', 'travel']

    if selected_categories:
        posts = Post.objects.filter(category__in=selected_categories)
    else:
        posts = Post.objects.all()

    categories = dict(Post.CATEGORY_CHOICES)  # {'tech': 'Tech', 'travel': 'Travel', ...}

    return render(request, 'blog/show_blog.html', {
        'posts': posts,
        'categories': categories,
        'selected_categories': selected_categories
    })


def edit_blog(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_blog.html', {'form': form, 'post': post})
def delete_blog(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('show_blog')  # ✅ without arguments

    return render(request, 'blog/delete_blog.html', {'post': post})

def about(request):
    return render(request, 'blog/about.html')