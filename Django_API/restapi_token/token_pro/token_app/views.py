from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer, FeedbackSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .models import Feedback


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Register Successfully"})
    return Response(serializer.errors)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user(request):
    data = User.objects.all()
    serializer = UserSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_user(request,id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message" : "User Not Found"})

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "User Updated Successfully"})
    return Response(serializer.errors)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message" : "User Not Found"})
    
    user.delete()
    return Response({"message" : "User Deleted Successfully"})


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Login Successfully",
                "token": token.key
            })

        return Response({
            "message": "Invalid Username or Password"
        })
    

class UserProfile(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = request.user
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    

@permission_classes([AllowAny])
class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackDetailView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]