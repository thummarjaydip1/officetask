from django.db import models
from users.models import CustomUser

class Event(models.Model):
    title = models.CharField()
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"


class Session(models.Model):
    title = models.CharField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)