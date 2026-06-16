from django.db.models.signals import post_save,pre_save,post_delete,pre_delete
from django.dispatch import receiver
from .models import *

@receiver(pre_save,sender=Student)
def before_save(sender,instance,**kwargs):
    print("Before Saved:",instance.name)

@receiver(post_save,sender=Student)
def after_save(sender,created,instance,**kwargs):
    if created:
        print("Student Created:", instance.name)
    else:
        print("Student Updated", instance.name)

@receiver(pre_delete,sender=Student)
def before_delete(sender,instance,**kwargs):
    print("Before Deleted:",instance.name)

@receiver(post_delete,sender=Student)
def after_delete(sender,instance,**kwargs):
    print("After Deleted:",instance.name)