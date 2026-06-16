from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField(max_length=150)


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    rating = models.CharField(
        default="Excellent",
        choices=(("Excellent", "Excellent"), ("Good", "Good"), ("Poor", "Poor")),
    )
    message = models.TextField()
