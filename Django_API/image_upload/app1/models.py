from django.db import models

class Student(models.Model):
    name= models.CharField()
    image= models.ImageField(upload_to="")

    def __str__(self):
        return self.name
    