from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from .models import *

def home(request):
    today = datetime.datetime.now()
    res = f"Today Date: {today.date()} and Time: {today.time()}"
    return render(request, "index.html", {"res":res})

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        city = request.POST.get("city")
        Student.objects.create(
            name = name,
            age = age,
            city = city
        )
        return redirect('display')
    return render(request, "add.html")

def display_student(request):
    students = Student.objects.all()
    return render(request, "display.html", {"students":students})

def update_student(request,id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        student.name = request.POST.get("name")
        student.age = request.POST.get("age")
        student.city = request.POST.get("city")
        student.save()
        return redirect("display")
    return render(request, "update.html", {"student":student})

def delete_student(request,id):
    student = Student.objects.get(id = id)
    student.delete()
    return redirect("display")