from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


# http://127.0.0.1:8000/api/add/
@api_view(["POST"])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Added Student data"})
    return Response(serializer.errors)


# http://127.0.0.1:8000/api/display/
@api_view(["GET"])
def display_student(request):
    data = Student.objects.all()
    serializer = StudentSerializer(data, many=True)
    return Response(serializer.data)


# http://127.0.0.1:8000/api/update/1/
@api_view(["PUT"])
def update_student(request, id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Student Data Updated Successfully"})
    return Response(serializer.errors)


# http://127.0.0.1:8000/api/delete/1/
@api_view(["DELETE"])
def delete_student(request, id):
    data = Student.objects.get(id=id)
    data.delete()
    return Response({"msg": "Student Record Deleted Successfully"})