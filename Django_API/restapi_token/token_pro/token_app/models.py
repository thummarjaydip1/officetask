from django.db import models

class Feedback(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    message = models.TextField()