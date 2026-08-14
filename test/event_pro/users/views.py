from django.shortcuts import render, redirect
from users.forms import UserForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def add_user(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_user")
    return render(request, "user_form.html", {"form":form})


def list_user(request):
    data = CustomUser.objects.all()
    return render(request, "user_list.html", {"data":data})


def update_user(request, id):
    user = CustomUser.objects.get(id=id)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("list_user")
    return render(request, "user_form.html", {"form":form})

def delete_user(request, id):
    data = CustomUser.objects.get(id=id)
    data.delete()
    return redirect("list_user")