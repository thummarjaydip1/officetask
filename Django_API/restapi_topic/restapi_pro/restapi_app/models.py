from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(max_length=50)
    address = models.TextField()
    