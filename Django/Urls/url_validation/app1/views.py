from django.shortcuts import render,redirect
from .forms import UrlForm
from .models import ValidateURL
from django.http import HttpResponse

def index(request):
    form = UrlForm()
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            ValidateURL.objects.create(url=url)
            return redirect("success")

    return render(request, "index.html", {'form':form})

def success(request):
    urls = ValidateURL.objects.all()
    return render(request, "success.html", {"urls":urls})