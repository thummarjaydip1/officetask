from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import *
from .serializers import *
import requests

API_URL ="http://127.0.0.1:8000/myapi/contact/"

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    # queryset = Employee.objects.all().order_by
    queryset =Employee.objects.all()
    serializer_class = EmployeeSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


def contact_form_add_data(request):
    if request.method == "POST":
        data={
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "email": request.POST.get("email"),
            "mobile": request.POST.get("mobile"),
            "address": request.POST.get("address")
        }
        requests.post(API_URL,json=data)
    return render(request,"index.html")

def contact_form_display_data(request):
    response = requests.get(API_URL)
    data = response.json()
    return render(request, "display.html", {"data":data})

def contact_form_update_data(request,id):
    if request.method == "POST":
        update_data={
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "email": request.POST.get("email"),
            "mobile": request.POST.get("mobile"),
            "address": request.POST.get("address")
        }
        requests.put(f"{API_URL}{id}/",data=update_data)
        return redirect('display')
    response = requests.get(f"{API_URL}{id}/")
    data = response.json()
    return render(request, "update.html", {"data":data})

def contact_form_delete_data(request,id):
    requests.delete(f"{API_URL}{id}/")
    return redirect('display')
