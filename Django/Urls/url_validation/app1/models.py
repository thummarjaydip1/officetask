from django.db import models

class ValidateURL(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
