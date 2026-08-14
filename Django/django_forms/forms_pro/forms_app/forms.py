from django import forms 
from .models import Student, FeedBack, Contact, Person, Book
from django.forms import modelformset_factory

class StudentForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    email = forms.EmailField()
    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ["name", "age", "message"]

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        message = cleaned_data.get("message")

        if name and len(name) <= 3:
            self.add_error('name', 'name minimum 3 character required')

        if message and len(message) <= 10:
            self.add_error('message', 'message minimum 10 character required')

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Enter Name'}),
            'age' : forms.TextInput(attrs={'placeholder' : 'Enter Age'}),
            'email' : forms.TextInput(attrs={'placeholder' : 'Enter Email'}),
        }


class PersonForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    city = forms.CharField()


BookForm = modelformset_factory(Book, fields=["title", "page", "description"])
