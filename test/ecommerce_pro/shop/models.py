from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.BigIntegerField()
    status = models.CharField(default="pending", choices=(
        ("pending","pending"),
        ("processing","processing"),
        ("shipped","shipped")
    ))
    phone = models.CharField(max_length=15)
    address = models.TextField()
    def __str__(self):
        return f"{self.products.name} - {self.user.username}" 