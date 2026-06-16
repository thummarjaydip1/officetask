from django.shortcuts import render
from django.core.cache import cache
from .models import *

def student_list(request):
    data = cache.get("student_data")

    if data is None:
        print("DB Hit")
        data = Student.objects.all().values()
        cache.set("stuednt_data",data,30)
    else:
        print("CACHE Hit")
    return render(request,'home.html',{"data":data})