from .models import Product
from django.dispatch import receiver
from django.db.models.signals import post_delete


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)
