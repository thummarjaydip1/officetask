from django.shortcuts import render
import datetime

def index(request):
    l1 = [11,22,33,44,55]
    context = {
        "data" : "hello user",
        "firstname": "jay",
        "lastname": "desai",
        'age': 21,
        "list" : l1
    }
    return render(request, "index.html",context)

def filter_page(request):
    dt = datetime.datetime.now().date()
    l1 = ["apple", "banana", "mango", 'kiwi']
    context = {
        'a': 21,
        "fname" : "jaydip",
        "lname" : "Thummar",        
        "dt" : dt,
        "city" : "",
        "description" : "hello wolrd",
        "l1" : l1,
        "a1" : "Don't distrub me",
        "string" : "Hello, How are you, welcome my profile",
        "dictionary" : [
            {"name" : "jay", "age" : 21},
            {"name" : "dip", "age" : 25},
            {"name" : "raj", "age" : 22},
            {"name" : "man", "age" : 23},
        ],
        "linenum" : """ Hey
                    Hello user,
                    Welcome to my profile,
                    How are you?
                    Bye."""
    }

    return render(request, "filter_page.html", context)


def boolean_operator(request):
    l1 = ["apple", "banana", "mango", "kiwi"]
    context = {
        "x" : 20,
        "y" : 30,
        "l1" :l1
    }
    return render(request, "boolean_operator.html", context)

def for_loop_temp(request):
    l1 = [11,22,33,44,55,66,77]
    d1 = {
        "name" : "jay",
        "age" : 21,
        "city" : "amreli"
    }
    context = {
        "l1" : l1,
        "d1" : d1
    }
    return render(request, "for_loop.html", context)


def if_else_temp(request):
    context = {
        "age" : 21
    }
    return render(request, "if_else.html", context)