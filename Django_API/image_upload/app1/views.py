from django.shortcuts import render,redirect
from .models import *
from .forms import *

def add_data(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('display')
    else:
        form = StudentForm()
    return render(request, "form.html",{"form":form})

def display_data(request):
    data = Student.objects.all()
    return render(request, "display.html",{"data":data})