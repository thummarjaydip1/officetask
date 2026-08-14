from django.shortcuts import render, redirect
from .forms import TagForm, PostForm, CommentFrom
from .models import Tag, Post, Comment


def index(request):
    tag = Tag.objects.all()
    post = Post.objects.all()
    comment = Comment.objects.all()

    context = {
        "tag" : tag,
        "post" : post,
        "comment" : comment
    }
    return render(request, "index.html", context)



def add_tag(request):
    form = TagForm()

    if request.method == "POST":
        form = TagForm(request.POST)
        
        if form.is_valid():
            form.save()
        return redirect("index")
    
    return render(request, "tag_form.html", {"form":form})



def update_tag(request, id):
    tag = Tag.objects.get(id=id)
    form = TagForm(instance=tag)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            form.save()
        return redirect('index')
    
    return render(request, "tag_form.html", {"form":form})



def delete_tag(request, id):
    data = Tag.objects.get(id=id)
    data.delete()
    return redirect('index')



def add_post(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('index')
    
    return render(request, "post_form.html", {"form":form})



def update_post(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
        return redirect('index')
    
    return render(request, "post_form.html", {"form":form})



def delete_post(request, id):
    data = Post.objects.get(id=id)
    data.delete()
    return redirect('index')



def add_comment(request):
    form = CommentFrom()

    if request.method == "POST":
        form = CommentFrom(request.POST)

        if form.is_valid():
            form.save()
        return redirect('index')

    return render(request, "comment_form.html", {"form":form})



def update_comment(request, id):
    comment = Comment.objects.get(id=id)
    form = CommentFrom(instance=comment)

    if request.method == "POST":
        form = CommentFrom(request.POST, instance=comment)

        if form.is_valid():
            form.save()
        return redirect('index')
    
    return render(request, "comment_form.html", {"form":form})



def delete_comment(request, id):
    data = Comment.objects.get(id=id)
    data.delete()
    return redirect('index')



def post_detail(request,id):
    post = Post.objects.get(id=id)
    comment = Comment.objects.filter(posts=post)
    return render(request, "post_detail.html", {"post":post, "comment":comment})