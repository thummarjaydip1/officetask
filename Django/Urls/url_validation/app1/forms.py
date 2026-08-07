from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(
        label="Enter url",
        widget= forms.TextInput(attrs={'placeholder' : 'https://example.com/'})
    )