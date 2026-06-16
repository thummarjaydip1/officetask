from django.shortcuts import render,redirect
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import requests

# http://127.0.0.1:8000/api/add-student/
@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"meg":"data added sucessfully"})
    return Response(serializer.errors)

# http://127.0.0.1:8000/api/get-student/
@api_view(['GET'])
def get_student(request):
    data = Student.objects.all()
    serializer = StudentSerializer(data, many=True)
    return Response(serializer.data)

# http://127.0.0.1:8000/api/get-student-id/5/
@api_view(['GET'])
def get_student_id(request, id):
    try:
        student = Student.objects.get(id=id)  
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

# http://127.0.0.1:8000/api/update-student/1/
@api_view(['PUT'])
def update_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"})

    serializer = StudentSerializer(student, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "updated successfully"})
    return Response(serializer.errors)

# http://127.0.0.1:8000/api/delete-student/2/
@api_view(['DELETE'])
def delete_student(request,id):
    try:
        student=Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error":"student not found"})
    student.delete()
    return Response({"msg":"Deleted Record"})

# CRUD operations
def student_add_data(request):
    ADD_API = "http://127.0.0.1:8000/api/add-student/"
    if request.method == "POST":
        data={
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "email": request.POST.get("email"),
            "branch": request.POST.get("branch")
        }
        requests.post(ADD_API,json=data)
        return redirect('student_display_data')
    return render(request,"student.html")


def student_display_data(request):
    VIEW_API = "http://127.0.0.1:8000/api/get-student/"
    response = requests.get(VIEW_API)
    data = response.json()
    return render(request,"display.html",{"data":data})

def student_update_data(request,id):
    UPDATE_API= "http://127.0.0.1:8000/api/update-student/"
    GET_API_ID = "http://127.0.0.1:8000/api/get-student-id/"
    if request.method == "POST":
        update_data={
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "email": request.POST.get("email"),
            "branch": request.POST.get("branch")
        }
        requests.put(f"{UPDATE_API}{id}/",json=update_data)
        return redirect('student_display_data')
    response = requests.get(f"{GET_API_ID}{id}/")
    data = response.json()
    return render(request,"update.html",{"data":data})

def student_delete_data(request,id):
    DELETE_API = "http://127.0.0.1:8000/api/delete-student/"
    response = requests.delete(f"{DELETE_API}{id}/")
    return redirect('student_display_data')