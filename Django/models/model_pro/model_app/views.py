from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("add model, update model, makemigrations and migrate command, model datatype and model field, Render rmodel in admin interface, django ORM, field validation and built in fields")