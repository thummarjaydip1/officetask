from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="images")
    auther = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name


class EmployeeRegister(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    age = models.IntegerField()
    positive_num = models.PositiveIntegerField()
    small_positive_num = models.PositiveSmallIntegerField()
    small_num = models.SmallIntegerField()
    email = models.EmailField()
    salary = models.BigIntegerField()
    image = models.ImageField(upload_to="images")
    cv = models.FileField(upload_to='cv/')
    float_num = models.FloatField()
    generic_IP = models.GenericIPAddressField()
    binary_field = models.BinaryField()
    slug_field = models.SlugField(max_length=200)
    message = models.TextField()
    url = models.URLField()
    time = models.TimeField()
    update_at = models.DateField(auto_now=True)
    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    editable = models.CharField(editable=False)
    username = models.CharField(error_messages={"unique":"please enter unique name"})
    password = models.CharField(help_text="please enter string password")
    address = models.CharField(verbose_name="city")


class Album(models.Model):
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Song(models.Model):
    name = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.name