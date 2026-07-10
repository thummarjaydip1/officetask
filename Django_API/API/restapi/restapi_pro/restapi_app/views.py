from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Student, Contact, Feedback
from .serializers import StudentSerializer, ContactSerializer, FeedbackSerializer

from rest_framework import viewsets
from rest_framework import generics


# ADD_API = http://127.0.0.1:8000/add-student/
@api_view(["POST"])
def add_student(request):
    serializer = StudentSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "Student added successfully"})

    return Response(serializer.errors)
 

# GET_API = http://127.0.0.1:8000/get-student/
@api_view(["GET"]) 
def get_student(request):
    data =  Student.objects.all()
    serializer = StudentSerializer(data, many = True)
    return Response(serializer.data)


# UPDATE_API = http://127.0.0.1:8000/update-student/2
@api_view(["PUT"])
def update_student(request, id):
    try:
        student = Student.objects.get(id = id)

    except Student.DoesNotExist:
        return Response({"message" : "Student does not exists"})

    serializer = StudentSerializer(student, data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message" : "Student record updated successfully"})
    
    return Response(serializer.errors)


# DELETE_API = http://127.0.0.1:8000/delete-student/2
@api_view(["DELETE"])
def delete_student(request, id):

    try:
        data = Student.objects.get(id = id)

    except Student.DoesNotExist:
        return Response({"message" : "Student does not exists"})
    
    data.delete()
    
    return Response ({
        "message" : "Student record deleted successfully"
    })


@api_view(["GET"])
def search_student(request):
    name = request.GET.get("name")

    students = Student.objects.all()
        
    if name:
        students = students.filter(name__icontains = name)

    serializer = StudentSerializer(students, many = True)
    return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@api_view(["POST"])
def add_feedback(request):
    serializer = FeedbackSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "messsge" : "Feedback send successfully",
            "added_feedback" : serializer.data
        })
    
    return Response(serializer.errors)


@api_view(["GET"])
def get_feedback(request):
    feedbacks = Feedback.objects.all()

    serializer = FeedbackSerializer(feedbacks, many = True)
    return Response(serializer.data)


@api_view(["PUT"])
def update_feedback(request, id):
    try:
        feedback = Feedback.objects.get(id = id)
    
    except:
        return Response({"message" : "Feedback not found"})

    serializer = FeedbackSerializer(feedback, data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Feedback update successfully",
            "updated_feedback" : serializer.data
        })
    
    return Response(serializer.errors)


@api_view(["DELETE"])
def delete_feedback(request, id):
    try:
        feedback = Feedback.objects.get(id = id)

    except:
        return Response({"message" : "Feedback not found"})
    
    feedback.delete()

    return Response({"message" : "Feedback deleted successfully"})


@api_view(["GET"])
def search_feedback(request):
    
    name = request.GET.get("name")

    feedbacks = Feedback.objects.all()

    if name:
        feedbacks.filter(name__icontains = name)

    serializer = FeedbackSerializer(feedbacks, many=True)

    return Response(serializer.data)
