from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StudentSerializer
from .models import Student


# RESTAPI

@api_view(["POST"])
def add_student(request):
    serializer = StudentSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "Student Record Added"})
    
    return Response(serializer.errors)


@api_view(["GET"])
def display_student(request):
    data = Student.objects.all()
    serializer = StudentSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def student_profile(request, id):
    data = Student.objects.get(id = id)
    serializer = StudentSerializer(data)
    return Response(serializer.data)


@api_view(["PUT"])
def update_student(request, id):
    try:
        student = Student.objects.get(id=id)
        
        serializer = StudentSerializer(student, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Student Record Updated"})
        
        return Response(serializer.errors)
    
    except Student.DoesNotExist:
        return Response({"message" :  "Student Record Does not Exists"})


@api_view(["DELETE"])
def delete_student(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return Response({"message" :  "Student Record Deleted Successfully"})
    
    except Student.DoesNotExist:
        return Response({"message" :  "Student Record Does not Exists"})


@api_view(["GET"])
def search_student(request):
    try:
        name = request.GET.get("name")
        age = request.GET.get("age")

        students = Student.objects.all()
        
        if name:
            students = students.filter(name__icontains = name)

        if age:
            students = students.filter(age = age)

        seralizer = StudentSerializer(students, many=True)
        return Response(seralizer.data)
    
    except:
        return Response({"message" : "Student Record Does not Exists"})


@api_view(["GET"])
def filter_student(reuqest):
    try:
        address = reuqest.GET.get("address")
        data = Student.objects.filter(address=address)
        serializer = StudentSerializer(data, many=True)
        return Response(serializer.data)

    except:
        return HttpResponse({"message" : "Student Record Does not Exists"})


@api_view(["GET"])
def count_student(request):
    student = Student.objects.count()
    return Response({
        "total student" : student
    })
