from django.shortcuts import render, redirect
from .models import Contact, PhoneNumber
from .forms import ContactForm, PhoneNumberForm

# contact
def add_contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("list_contact")
    return render(request, "contact_form.html", {"form":form})


def list_contact(request):
    contact = Contact.objects.all()
    return render(request, "contact_list.html", {"contact":contact})


def detail_contact(request, id):
    contact = Contact.objects.get(id = id)
    
    phone = PhoneNumber.objects.filter(contact=contact)

    return render(request, "contact_detail.html", {"contact":contact, "phone":phone})


def update_contact(request, id):
    contact = Contact.objects.get(id=id)
    form = ContactForm(instance=contact)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
        return redirect("list_contact")
    return render(request, "contact_form.html", {"form":form})


def delete_contact(request, id):
    data = Contact.objects.get(id = id)
    data.delete()
    return redirect("list_contact")


# phone number
def add_phonenum(request):
    form = PhoneNumberForm()
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("list_contact")
    return render(request, "phonenum_form.html", {"form":form})


def update_phonenum(request, id):
    phone = PhoneNumber.objects.get(id = id)
    form = PhoneNumberForm(instance=phone)
    if request.method == "POST":
        form = PhoneNumberForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
        return redirect ("list_contact")
    return render(request, "phonenum_form.html", {"form":form})

def delete_phonenum(request, id):
    data = PhoneNumber.objects.get(id = id)
    data.delete()
    return redirect("list_contact")