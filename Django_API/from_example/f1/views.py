# function thi crud operations
from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from f1.models import Contact,Feedback
# class thi crud operations
from f1.models import Student
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

# function
def home(request):
    data = Contact.objects.all()
    data1= Feedback.objects.all()
    return render(request, "index.html",{"data":data,"data1":data1})

def contact_add(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, "contact.html", {"form": form})

def contact_update(request,id):
    contact= get_object_or_404(Contact,id=id)
    form = ContactForm(instance=contact)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,"contact.html",{"form":form})

def contact_delete(request,id=id):
    contact = get_object_or_404(Contact,id=id)
    contact.delete()
    return redirect('home')

def feedback_add(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "feedback.html",{"form":form})

def feedback_update(request,id):
    feedback= get_object_or_404(Feedback,id=id)
    form = FeedbackForm(instance=feedback)
    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "feedback.html",{"form":form})

def feedback_delete(request,id):
    feedback = get_object_or_404(Feedback,id=id)
    feedback.delete()
    return redirect('home')


# class 
class StudentListview(ListView):
    model = Student
    template_name = "student_list.html"
    context_object_name = "data2"

class StudentCreateView(CreateView):
    model = Student
    fields = "__all__"
    template_name = "student.html"
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    fields = "__all__"
    template_name = 'student.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student_list')