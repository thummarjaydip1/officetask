from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    print("index function", request.POST)
    return JsonResponse({"message":"Hello World"})