from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# @api_view(['GET'])    
def my_view(request):
    print("view executed")
    # return Response({"msg":"Hello View!"})
    return HttpResponse("Hello View!")

def test_view(request):
    return HttpResponse("Test view")

def template_view(request):
    return TemplateResponse(request, "home.html", {})

def exception_view(request):
    x=10/0
    return HttpResponse("this want run")