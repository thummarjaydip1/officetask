from django import forms
from .models import Post, Tag, Comment


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'publication_date' : forms.DateInput(attrs={"type" : "date"})
        }

class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
