from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from django.db.models import Avg, Count, Sum

# <----- get() method ------>
# def home(request):
#     try:
#         a = Student.objects.get(city="surat")
#     except Student.DoesNotExist:
#         print("student not found")
#     except Student.MultipleObjectsReturned:
#         print("multiple object returned")
#     return HttpResponse("hello")

# def home(request):
#     try: 
#         a = Student.objects.get(id = 3, city="surat")
#     except Student.DoesNotExist:
#         print("student record not found")
#     return HttpResponse("hello")


# <----- filter() and exclude() and Q method ------>
# def home(request):
#     try:
#         stu = Student.objects.filter(city='surat')
#         print(stu)
#     except Student.DoesNotExist:
#         print("student not found")
#     return HttpResponse("hello")

# def home(request):
#     try:
#         stu = Student.objects.filter(city="surat").exclude(age=23)
#         print(stu)
#     except Student.DoesNotExist:
#         print('not found')
#     return HttpResponse("hello")


# def home(request):
#     try:
#         stu = Student.objects.filter(Q(city="surat")|(Q(city="junagadh")))
#         print(stu)
#     except Student.DoesNotExist:
#         print("student not found")
#     return HttpResponse("hello")


# <----- order_by() method ------>
# def home(request):
#     stu = Student.objects.all().order_by("age")
#     for i in stu:
#         print(i.name, i.age, i.city)

#     return HttpResponse("Ascending ")

# def home(request):
#     stu = Student.objects.all().order_by("-age")
#     for i in stu:
#         print(i.name, i.age, i.city)
#     return HttpResponse("Descending")

# def home(request):
#     stu = Student.objects.all().order_by("age").reverse()
#     for i in stu:
#         print(i.name, i.age, i.city)
#     return HttpResponse("Alternative Descending")

# def home(request):
#     stu = Student.objects.all().order_by("name", "age")
#     for i in stu:
#         print(i.name, i.age, i.city)
#     return HttpResponse("multiple sort")


# <----- aggregate() method ------>

# def home(request):
#     summary = Book.objects.aggregate(
#         total_books = Count('id'),
#         average_price = Avg('price'),
#         total_price = Sum('price')
#     )
#     print(summary)
#     return HttpResponse('aggregate() method')


# <----- annotate() method ------>

def home(request):
    auther_summery = Author.objects.annotate(
        total_books = Count('books'),
        total_price = Sum('books__price')
    )
    for i in auther_summery:
        print(f"Auther name: {i.name}, total books: {i.total_books}, total price: {i.total_price:.2f}")
    return HttpResponse("annotate() method")