from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return redirect("login")
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            return redirect("login")
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def profile(request):
    data = Profile.objects.get(user=request.user)
    return render(request,"profile.html", {"data" : data})