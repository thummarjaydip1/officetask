from django.shortcuts import render
import requests

def home(request):

    DATA_API = "http://127.0.0.1:8000/user/display"
    username = request.GET.get("username")
    if username:
        SEARCH_API = f"http://127.0.0.1:8000/user/search?username={username}"
        res = requests.get(SEARCH_API)

    else:
        res = requests.get(DATA_API)

    data = res.json()

    return render(request,"home.html",{"data":data})