from django.shortcuts import render, redirect
from .models import Book

def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        public_date = request.POST.get("public_date")
        Book.objects.create(
            title = title,
            author = author,
            public_date = public_date
        )
        return redirect("list")
    return render(request, "add_book.html")


def list_book(request):
    book = Book.objects.all()
    return render(request, "list_book.html", {"book":book})


def detail_book(request, id):
    data = Book.objects.get(id = id)
    return render(request, "detail_book.html", {"data" : data})


def update_book(request, id):
    book = Book.objects.get(id = id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.public_date = request.POST.get("public_date")
        book.save()
        return redirect("list")
    return render(request, "update_book.html", {"book":book})


def delete_book(request, id):
    data = Book.objects.get(id = id)
    data.delete()
    return redirect("list")