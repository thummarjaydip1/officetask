from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,get_user_model


User = get_user_model()

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            address=address
        )
        return redirect('login')
    return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("list_user")
        else:
            return redirect("login")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


def list_user(request):
    user = request.user
    data = User.objects.all()
    return render(request, "list.html", {"user":user,"data":data})