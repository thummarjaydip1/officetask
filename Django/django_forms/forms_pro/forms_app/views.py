from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm, FeedbackForm, ContactForm, PersonForm, BookForm
from django.forms import formset_factory, modelformset_factory
from .models import Book

def student_form(request):
    form = StudentForm()
    return render(request, "student.html", {"form":form})


def feedback_form(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Data Send Successfully")
    return render(request, "feedback.html", {"form":form})


def contact_form(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Date Send Successfully")
    return render(request, "contact.html", {"form":form})


def person_form(request):
    PersonFormSet = formset_factory(PersonForm)
    form = PersonFormSet()
    return render(request, "person.html", {"form": form})


def book_form(request):
    BookFormSet = modelformset_factory(Book, fields=['title', 'page', 'description'], extra=0)
    form = BookFormSet()
    if request.method == "POST":
        form = BookFormSet(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Save Book data...")
    return render(request, "book.html", {"form":form})