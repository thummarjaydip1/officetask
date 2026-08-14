from django.db import models

class Contact(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    type_phone = models.CharField(choices=(
        ("home","home"),
        ("work","work"),
        ("mobile","mobile")
    ))