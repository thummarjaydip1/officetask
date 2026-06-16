from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

User = get_user_model()

def register_user(request):
    if request.method == "POST":
        username= request.POST.get("username")
        password= request.POST.get("password")
        firstname= request.POST.get("firstname")
        lastname= request.POST.get("lastname")
        email= request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        
        User.objects.create_user(username=username,
                                 password=password,
                                 first_name=firstname,
                                 last_name=lastname,
                                 email=email,
                                 phone=phone,
                                 address=address)
        return redirect('login')

    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("invalid username password")
            return redirect('login')
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    return render(request, "home.html")