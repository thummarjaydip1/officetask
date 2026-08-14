from django import forms
from .models import Event, Attendee, Session

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'start_time' : forms.DateTimeInput(attrs={"type" : "datetime-local"}),
            'end_time' : forms.DateTimeInput(attrs={"type" : "datetime-local"})
        }



class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = "__all__"

        
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = "__all__"
        widgets = {
            'start_time' : forms.DateTimeInput(attrs={"type" : "datetime-local"}),
            'end_time' : forms.DateTimeInput(attrs={"type" : "datetime-local"})
        }