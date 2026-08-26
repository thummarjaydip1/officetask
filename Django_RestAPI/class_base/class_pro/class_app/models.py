from django.db import models

class Contact(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()


class Feedback(models.Model):
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()


class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    city = models.CharField()
    image = models.ImageField(upload_to="students")


class Employee(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    city = models.TextField()