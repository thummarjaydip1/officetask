from django.shortcuts import render,redirect
from .models import Student
from .forms import StudentForm

def add_student(request):
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("display")
    return render(request, "student_form.html", {"form":form})


def display_student(request):
    student = Student.objects.all()
    return render(request, "student_display.html", {"student":student})

def detail_student(request,id):
    student = Student.objects.get(id = id)
    return render(request, "student_detail.html", {"student":student})


def update_student(request,id):
    student = Student.objects.get(id=id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
        return redirect("display")
    return render(request, "student_form.html", {"form":form})

def delete_student(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("display")