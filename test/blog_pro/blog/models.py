from django.db import models

class Tag(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    publication_date = models.DateField()
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField()
    email = models.EmailField()
    content = models.TextField()
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    