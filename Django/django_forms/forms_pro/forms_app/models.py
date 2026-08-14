from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()


class FeedBack(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    message = models.TextField()

class Contact(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()


class Person(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    city = models.CharField()


class Book(models.Model):
    title = models.CharField()
    page = models.IntegerField()
    description = models.TextField()