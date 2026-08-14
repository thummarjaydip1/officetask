from django import forms
from .models import Contact, PhoneNumber

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = "__all__"