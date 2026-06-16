from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
import requests

# http://127.0.0.1:8000/register_api/
@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Register Successfully"})
    return Response(serializer.errors)

# http://127.0.0.1:8000/login_api/
@api_view(['POST'])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username = username, password = password)
    if user is not None:
        login(request,user)
        return Response({"message":"Login Successfully"})
    return Response({"message":"Login Failled"})

# http://127.0.0.1:8000/logout_api/
@api_view(['POST'])
def logout_api(request):
    logout(request)
    return Response({"message":"Logout Suceessfully"})

# http://127.0.0.1:8000/user_display_api/
@api_view(['GET'])
def user_display_api(request):
    data = User.objects.all()
    serializer = RegisterSerializer(data, many=True)
    return Response(serializer.data)

# http://127.0.0.1:8000/user_display_id_api/10/
@api_view(['GET'])
def user_display_id_api(request,id):
    data = User.objects.get(id=id)
    serializer = RegisterSerializer(data)
    return Response(serializer.data)

# http://127.0.0.1:8000/user_update_api/10/
@api_view(['PUT'])
def user_update_api(request,id):
    user = User.objects.get(id=id)
    serializer = RegisterSerializer(user,data=request.data)
    if serializer.is_valid():
        user.username = serializer.validated_data["username"]
        user.email = serializer.validated_data["email"]
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response({"message":"Updated User"})
    return Response(serializer.errors)

# http://127.0.0.1:8000/user_delete_api/10/
@api_view(['DELETE'])
def user_delete_api(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return Response({"message":"Deleted User"})


# pages fronted
def auth_register(request):
    if request.method == "POST":
        data ={
            "username" : request.POST.get("username"),
            "password" : request.POST.get("password"),
            "email" : request.POST.get("email")
        }
        requests.post("http://127.0.0.1:8000/register_api/",data=data)
        return redirect("login")
    return render(request,"register.html")

def auth_login(request):
    if request.method == "POST":
        data = {
            "username" : request.POST.get("username"),
            "password" : request.POST.get("password")
        }
        res = requests.post("http://127.0.0.1:8000/login_api/",data=data)
        res.json()
        user = authenticate(
            username = data["username"],
            password = data["password"]
        )
        if user is not None:
            login(request,user)
            return redirect("index")
    return render(request,"login.html")

def auth_logout(request):
    # requests.post("http://127.0.0.1:8000/logout_api/")
    logout(request)
    return redirect("index")

def index(request):
    data = requests.get("http://127.0.0.1:8000/user_display_api").json()
    return render(request,"index.html",{"data":data})

def user_update(request,id):
    if request.method == "POST":
        updated_data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "email": request.POST.get("email")
        }
        requests.put(f"http://127.0.0.1:8000/user_update_api/{id}/",data=updated_data)
        return redirect("index")
    res = requests.get(f"http://127.0.0.1:8000/user_display_id_api/{id}/")
    data = res.json()
    return render(request,"update_user.html",{"data":data})

def user_delete(request,id):
    if request.user.id == id:
        requests.delete(f"http://127.0.0.1:8000/user_delete_api/{id}/")
        logout(request)
    return redirect('index')
    
def profile(request):
    data = {}
    if request.user.is_authenticated:
        data = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        }
    return render(request,"profile.html",{"data":data})