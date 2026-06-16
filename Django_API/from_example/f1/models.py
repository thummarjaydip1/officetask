from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    mobile = models.IntegerField()

class Feedback(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    rating = models.CharField(choices=(
        ('excellent','excellent'),
        ('good','good'),
        ('not good','not good')
    ))
    message = models.TextField()

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
