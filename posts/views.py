from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Post, Like, Follow, Comment
from .forms import PostForm, CommentForm

def feed(request):
    if request.user.is_authenticated:
        following_ids = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
        posts = Post.objects.filter(Q(author__in=following_ids) | Q(author=request.user))\
                            .order_by('-created_at')[:50]
    else:
        posts = Post.objects.all().order_by('-created_at')[:50]
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # ¡request.FILES es clave!
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/post_new.html', {'form': form})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('feed')

@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        obj, created = Follow.objects.get_or_create(follower=request.user, followed=target)
        if not created:
            obj.delete()
    return redirect('feed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.post = post
            c.save()
    return redirect('feed')
