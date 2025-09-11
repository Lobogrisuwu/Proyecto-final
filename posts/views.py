# posts/views.py
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm

SESSION_TOKEN_KEY = "guest_token"
SESSION_NAME_KEY  = "guest_name"

def _ensure_guest(request):
    """
    Garantiza que la sesión tenga un token y, si no hay nombre, obliga a entrar a 'start'.
    """
    token = request.session.get(SESSION_TOKEN_KEY)
    name  = request.session.get(SESSION_NAME_KEY)
    if not token:
        # crea token
        token = uuid.uuid4().hex
        request.session[SESSION_TOKEN_KEY] = token
    if not name:
        return redirect('start')
    return token, name

def start(request):
    """
    Pantalla para escribir solo el nombre de usuario temporal.
    """
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        if 1 <= len(name) <= 30:
            if not request.session.get(SESSION_TOKEN_KEY):
                request.session[SESSION_TOKEN_KEY] = uuid.uuid4().hex
            request.session[SESSION_NAME_KEY] = name
            return redirect('feed')
    return render(request, 'start.html')

def logout_temp(request):
    """
    Salir: borra nombre y opcionalmente borra todas las publicaciones de ese token.
    """
    token = request.session.get(SESSION_TOKEN_KEY)
    # Si quieres borrar TODO del usuario al salir, descomenta:
    # if token:
    #     for p in Post.objects.filter(owner_token=token):
    #         p.delete()

    request.session.pop(SESSION_NAME_KEY, None)
    # NO borramos el token para mantener 'likes' previos si regresa dentro de la hora.
    return redirect('start')

def feed(request):
    # Purga ligera (opcional) al entrar al feed
    Post.objects.filter(expires_at__lte=timezone.now()).delete()

    posts = (Post.objects
             .filter(expires_at__gt=timezone.now())
             .annotate(likes_count=Count('likes'))
             .order_by('-created_at')[:50])
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'guest_name': request.session.get(SESSION_NAME_KEY),
    })

def post_new(request):
    res = _ensure_guest(request)
    if isinstance(res, redirect.__class__):  # si redirigió a start
        return res
    token, name = res

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner_token = token
            p.owner_name = name
            p.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/post_new.html', {'form': form})

@require_POST
def add_comment(request, post_id):
    res = _ensure_guest(request)
    if isinstance(res, redirect.__class__):
        return res
    token, name = res

    post = get_object_or_404(Post, id=post_id, expires_at__gt=timezone.now())
    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.post = post
        c.owner_token = token
        c.owner_name = name
        c.save()
    return redirect('feed')

def toggle_like(request, post_id):
    res = _ensure_guest(request)
    if isinstance(res, redirect.__class__):
        return res
    token, _ = res

    post = get_object_or_404(Post, id=post_id, expires_at__gt=timezone.now())
    like = Like.objects.filter(post=post, owner_token=token).first()
    if like:
        like.delete()
    else:
        Like.objects.create(post=post, owner_token=token)
    return redirect('feed')

# ---- Purga manual (para pruebas rápidas)
def purge_now(request):
    Post.objects.filter(expires_at__lte=timezone.now()).delete()
    return redirect('feed')
