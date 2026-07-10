from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    city = models.CharField()

class Contact(models.Model):
    name = models.CharField()
    email = models.EmailField()
    phone = models.CharField()
    address = models.TextField()

class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=150)