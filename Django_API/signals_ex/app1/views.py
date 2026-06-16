from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def create_student(request):
    Student.objects.create(name="jaydip",age=21)
    return HttpResponse("Student Created")

def updated_student(request):
    student = Student.objects.get(name="jaydip")
    # student = Student.objects.first()
    student.name = "JAYDIP"
    student.save()
    return HttpResponse("Student Updated")

def delete_student(request):
    student = Student.objects.get(name="JAY")
    # student = Student.objects.first()
    student.delete()
    return HttpResponse("Student Deleted")