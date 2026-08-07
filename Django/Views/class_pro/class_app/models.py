from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    city = models.CharField()