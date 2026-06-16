from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

User = get_user_model()


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("index")
        else:
            messages.warning(request, "Login Unsuccessfully")
            return redirect("auth_login")

    return render(request, "account/auth-login-basic.html")


def auth_register(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            contact = request.POST.get("contact")
            role = request.POST.get("role")
            password = request.POST.get("password")

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.contact = contact
            user.role = role
            user.save()
            messages.success(request, "Register Suceesfully")
            return redirect("auth_login")
        return render(request, "account/auth-register-basic.html")
    except:
        messages.warning(request, "Registration error")
        return redirect("error_page")


def auth_forget_password(request):
    data = request.user.username
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your Password Changed")
            return redirect("auth_login")
        except User.DoesNotExist:
            messages.warning(request, "User not Exit")
            return redirect("auth_forget_password")
    return render(request, "account/auth-forgot-password-basic.html", {"data": data})


@login_required(login_url="auth_login")
def auth_logout(request):
    logout(request)
    messages.warning(request, "Logout Successfully")
    return redirect("index")


def privacy_policy(request):
    return render(request, "account/privacy_policy.html")


@login_required(login_url="auth_login")
def auth_profile(request):

    profile = Profile.objects.get(user=request.user)

    res = requests.get(
        "https://www.timeapi.io/api/v1/time/current/zone?timeZone=Asia/Kolkata"
    )

    data = res.json()

    return render(
        request,
        "account/profile.html",
        {
            "profile": profile,
            "data": data,
        },
    )


@login_required(login_url="auth_login")
def auth_profile_edit(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.contact = request.POST.get("contact")
        user.role = request.POST.get("role")
        user.save()
        messages.success(request, "Profile Change Successfully")
        return redirect("auth_profile")
    return render(request, "account/profile_edit.html", {"user": user})
