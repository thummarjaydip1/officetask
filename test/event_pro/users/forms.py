from django import forms 
from .models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]
        