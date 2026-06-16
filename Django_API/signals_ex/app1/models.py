from django.db import models

class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()

    def __str__(self):
        return self.name