from django.db import models
from account.models import *
from product.models import *


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    total_price = models.IntegerField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
        ),
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total_price = self.price * self.quantity
        discount = (self.total_price * 5) / 100
        self.total_price = int(self.total_price - discount)
        super().save(*args, **kwargs)


class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
