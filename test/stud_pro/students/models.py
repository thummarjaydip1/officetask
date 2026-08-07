from django.db import models


class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    grade = models.CharField()