from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from .models import Post, Category
from django.db.models import Q


# Base template render
def base(request):
    return render(request, 'blog/base.html')


# Home page with optional category filter
@login_required
def home(request):
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category__id=category_id).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')[:3]

    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})


# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# Show all blogs with search and pagination
@login_required
def show_blog(request):
    query = request.GET.get('q', '')
    selected_categories = request.GET.getlist('category')
    
    posts = Post.objects.all().order_by('-created_at') 
    
    if selected_categories:
        posts = posts.filter(category__in=selected_categories)
    
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    paginator = Paginator(posts, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = dict(Post.CATEGORY_CHOICES)
    
    return render(request, 'blog/show_blog.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'query': query
    })


# View a single blog post
@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # Unlike
    else:
        post.likes.add(request.user)  # Like

    return redirect('post_detail', id=pk)


# Edit a blog post
@login_required
def edit_blog(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_blog.html', {'form': form, 'post': post})


# Delete a blog post
@login_required
def delete_blog(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('show_blog')
    return render(request, 'blog/delete_blog.html', {'post': post})


# User authentication views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'blog/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Already logged in

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
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'blog/register.html')


# Logout
@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')


# About page
login_required
def about(request):
    return render(request, 'blog/about.html')
