# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profile  # 👈 correcto: desde accounts.models

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asegura que exista el Profile
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("feed")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
