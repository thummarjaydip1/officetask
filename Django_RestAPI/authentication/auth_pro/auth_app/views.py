from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User Registration Successfully"})
    return Response(serializer.errors)

@api_view(["GET"])
def get_user(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message" : "User Does not Exists"})

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "User Update Successfully"})
    return Response(serializer.errors)

@api_view(["DELETE"])
def delete_update(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message" : "User Does not Exists"})
    
    user.delete()
    return Response({"message" : "User Deleted Successfully"})


class LoginAPIView(APIView):
    # permission_classes = []
    def post(self, request):
        
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response({
                "message" : "Login Successfully",
                "Token" : token.key
            })
        return Response({
            "message" : "Invalid Username"
        })
