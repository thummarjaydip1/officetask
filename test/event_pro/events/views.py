from django.shortcuts import render, redirect
from .models import Event, Attendee, Session
from .forms import EventForm, AttendeeForm, SessionForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def index(request):
    return render(request, "index.html")

def add_event(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_event")
    return render(request, "event_form.html", {"form":form})


def list_event(request):
    data = Event.objects.all()
    return render(request, "event_list.html", {"data":data})


def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("list_event")
    return render(request, "event_form.html", {"form":form})


def delete_event(request, id):
    data = Event.objects.get(id=id)
    data.delete()
    return redirect("list_event")


def detail_event(request, id):
    event = Event.objects.get(id=id)
    attendee = Attendee.objects.filter(event=event)
    session = Session.objects.filter(event=event)
    user = CustomUser.objects.get(email=event.user.email)
    context = {
        "event" : event,
        "attendee" : attendee,
        "session" : session,
        "user" : user
    }
    return render(request, "event_detail.html", context)


def add_attendee(request):
    form = AttendeeForm()
    if request.method == "POST":
        form = AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_attendee")
    return render(request, "attendee_form.html", {"form":form})


def list_attendee(request):
    data = Attendee.objects.all()
    return render(request, "attendee_list.html", {"data":data})


def update_attendee(request, id):
    attendee = Attendee.objects.get(id=id)
    form = AttendeeForm(instance=attendee)
    if request.method == "POST":
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            form.save()
            return redirect("list_attendee")
    return render(request, "attendee_form.html", {"form":form})


def delete_attendee(request, id):
    data = Attendee.objects.get(id=id)
    data.delete()
    return redirect("list_attendee")


def add_session(request):
    form = SessionForm()
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_session")
    return render(request, "session_form.html", {"form":form})


def list_session(request):
    data = Session.objects.all()
    return render(request, "session_list.html", {"data":data})


def update_session(request, id):
    session = Session.objects.get(id=id)
    form = SessionForm(instance=session)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect("list_session")
    return render(request, "session_form.html", {"form":form})


def delete_session(request, id):
    data = Session.objects.get(id=id)
    data.delete()
    return redirect("list_session")