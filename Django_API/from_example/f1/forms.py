from .models import *
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"