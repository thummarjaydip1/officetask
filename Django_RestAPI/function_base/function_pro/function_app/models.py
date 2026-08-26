from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    pocket_money = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to="students")
    birth_date = models.DateField()
