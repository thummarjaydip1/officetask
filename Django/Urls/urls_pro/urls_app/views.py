from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

class ProductListView(View):
    def get(self, request):
        return HttpResponse('all product display...')