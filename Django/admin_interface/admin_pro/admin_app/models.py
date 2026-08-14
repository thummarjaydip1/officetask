from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    addres = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
    page = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"