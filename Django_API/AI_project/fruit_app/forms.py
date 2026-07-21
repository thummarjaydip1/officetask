from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Contact


class CustomUserCreationForm(UserCreationForm):
    """Registration form with Full Name, Username, Email, and Phone fields."""
    
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists. Please choose a different username.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered. Please use a different email.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match. Please enter the same password.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('full_name').split()[0]
        user.last_name = ' '.join(self.cleaned_data.get('full_name').split()[1:]) if len(self.cleaned_data.get('full_name').split()) > 1 else ''
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Login form with custom styling and email lookup."""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username or email',
            'autofocus': True,
        })
    )
    
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                # if username is not found, try email authentication
                try:
                    user_obj = User.objects.get(email__iexact=username)
                except User.DoesNotExist:
                    user_obj = None

                if user_obj:
                    user = authenticate(self.request, username=user_obj.username, password=password)

            if user is None:
                raise ValidationError('Invalid username/email or password. Please try again.')
            if not user.is_active:
                raise ValidationError('This account is inactive. Please contact support.')

            self.confirm_login_allowed(user)
            self.user_cache = user

        return self.cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Please enter your name.')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Please enter your email.')
        return email

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise ValidationError('Please enter a subject.')
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise ValidationError('Please enter a message.')
        return message
