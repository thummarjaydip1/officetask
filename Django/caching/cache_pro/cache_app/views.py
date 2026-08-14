from django.shortcuts import render
from .models import *
from django.views.decorators.cache import cache_page

# @cache_page(60)           60 second cache memory
# @cache_page(60 * 2)       120 second means 2 minute cache memory
# @cache_page(60 * 60)      3600 second means 60 minute means 1 hour cache memory


@cache_page(60)
def list_student(request):
    print("database in enter")
    student = Student.objects.all()
    return render(request, 'index.html', {"student":student})
