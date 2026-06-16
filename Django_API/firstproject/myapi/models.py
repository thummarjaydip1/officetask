from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    type = models.CharField(max_length=100,choices=(
        ('IT','IT'),
        ('NON IT','NON IT'),
        ('MOBILE PHONE','MOBILE PHONE')))
    added_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


#employee model
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    email = models.EmailField()
    address = models.CharField()
    phone = models.CharField()
    about = models.TextField()
    position = models.CharField(choices=(
        ('Manager','manager'),
        ('Software Developer','Software Developer'),
        ('Project leader','Project Developer')
    ))
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

#contact model api
class Contact(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField()
    mobile = models.IntegerField()
    address = models.TextField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)