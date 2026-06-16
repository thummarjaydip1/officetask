from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer, FeedbackSerializer
import requests


# CONTACT table with API
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


CONTACT_API = "http://127.0.0.1:8000/api/api/contact-api/"


@login_required(login_url="auth_login")
def contact_add_data(request):
    try:
        if request.method == "POST":
            data = {
                "name": request.POST.get("name"),
                "age": request.POST.get("age"),
                "email": request.POST.get("email"),
                "mobile": request.POST.get("mobile"),
                "address": request.POST.get("address"),
            }
            requests.post(CONTACT_API, json=data)
            messages.success(request, "Contact Send Successfully")
            return redirect("display_data")
        return render(request, "api/contact.html")
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")


@login_required(login_url="auth_login")
def contact_update_data(request, id):
    try:
        response = requests.get(f"{CONTACT_API}{id}/")
        data = response.json()
        if request.user.username == data["name"]:
            if request.method == "POST":
                update_data = {
                    "name": request.POST.get("name"),
                    "age": request.POST.get("age"),
                    "email": request.POST.get("email"),
                    "mobile": request.POST.get("mobile"),
                    "address": request.POST.get("address"),
                }
                requests.put(f"{CONTACT_API}{id}/", data=update_data)
                messages.success(request, "Contact Update Successfully")
                return redirect("display_data")
        else:
            messages.warning(request, "You cant update only your contact")
            return redirect("error_page")
        return render(request, "api/contact_update.html", {"data": data})
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")


@login_required(login_url="auth_login")
def contact_delete_data(request, id):
    try:
        response = requests.get(f"{CONTACT_API}{id}/")
        data = response.json()
        if request.user.username == data["name"]:
            requests.delete(f"{CONTACT_API}{id}/")
            messages.warning(request, "Contact Delete Successfully")
            return redirect("display_data")
        else:
            messages.warning(request, "You cant delete only your contact")
            return redirect("error_page")
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")


@login_required(login_url="auth_login")
def display_data(request):
    try:
        # contact table data display api throw
        response = requests.get(CONTACT_API)
        data = response.json()

        # feedback table data display api throw
        FEEDBACK_DISPLAY_DATA = "http://127.0.0.1:8000/api/api/feedback-display/"
        responsee = requests.get(FEEDBACK_DISPLAY_DATA)
        dataa = responsee.json()
        return render(request, "api/con_fed_disp.html", {"data": data, "dataa": dataa})
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")


# FEEDBACK table with API
@api_view(["POST"])
def feedback_add(request):
    serializer = FeedbackSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Added Successfully"})

    return Response(serializer.errors)


@api_view(["GET"])
def feedback_display(request):
    data = Feedback.objects.all()
    serializer = FeedbackSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def feedback_display_id(request, id):
    data = Feedback.objects.get(id=id)
    serializer = FeedbackSerializer(data)
    return Response(serializer.data)


@api_view(["PUT"])
def feedback_update(request, id):
    feedback = Feedback.objects.get(id=id)
    serializer = FeedbackSerializer(feedback, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Record Updated Successfully"})
    return Response(serializer.errors)


@api_view(["DELETE"])
def feedback_delete(request, id):
    data = Feedback.objects.get(id=id)
    data.delete()
    return Response({"msg": "Record Deleted Successfully"})


@login_required(login_url="auth_login")
def feedback_add_data(request):
    try:
        FEEDBACK_ADD_API = "http://127.0.0.1:8000/api/api/feedback-add/"
        if request.method == "POST":
            data = {
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "rating": request.POST.get("rating"),
                "message": request.POST.get("message"),
            }
            requests.post(FEEDBACK_ADD_API, data=data)
            messages.success(request, "Feedback Send Successfully")
            return redirect("display_data")
        return render(request, "api/feedback.html")
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")


@login_required(login_url="auth_login")
def feedback_update_data(request, id):
    try:
        FEEDBACK_UPDATE_API = "http://127.0.0.1:8000/api/api/feedback-update/"
        FEEDBACK_DISPLAY_ID = "http://127.0.0.1:8000/api/api/feedback-display-id/"
        response = requests.get(f"{FEEDBACK_DISPLAY_ID}{id}/")
        data = response.json()
        if request.user.username == data["name"]:
            if request.method == "POST":
                update_data = {
                    "name": request.POST.get("name"),
                    "email": request.POST.get("email"),
                    "rating": request.POST.get("rating"),
                    "message": request.POST.get("message"),
                }
                requests.put(f"{FEEDBACK_UPDATE_API}{id}/", json=update_data)
                messages.success(request, "Feedbcak Update Successfully")
                return redirect("display_data")
        else:
            messages.warning(request, "You cant update only your feedback")
            return redirect("error_page")
        return render(request, "api/feedback_update.html", {"data": data})
    except:
        messages.warning(request, "Somthing wrong")


def feedback_delete_data(request, id):
    try:
        FEEDBACK_DELETE = "http://127.0.0.1:8000/api/api/feedback-delete/"
        FEEDBACK_DISPLAY_ID = "http://127.0.0.1:8000/api/api/feedback-display-id/"
        response = requests.get(f"{FEEDBACK_DISPLAY_ID}{id}/")
        data = response.json()
        if request.user.username == data["name"]:
            requests.delete(f"{FEEDBACK_DELETE}{id}/")
            messages.warning(request, "Record Deleted Successfully")
            return redirect("display_data")
        else:
            messages.warning(request, "You cant delete only your feedback")
            return redirect("error_page")
    except:
        messages.warning(request, "Somthing wrong")
        return redirect("error_page")
