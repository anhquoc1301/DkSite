from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    create_at = models.DateTimeField(auto_now_add=True)
    code=models.IntegerField(null=True)
    is_admin=models.BooleanField(default=False)


class Product(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    owner=models.IntegerField(default=0)
    code=models.IntegerField(null=False)
    type_item=models.IntegerField()
    country=models.CharField(max_length=40)
    prime=models.IntegerField()
    state=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    information=models.CharField(max_length=1000)
    pending=models.BooleanField(default=False)


class waitaccept(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    user=models.IntegerField(null=False)
    product=models.IntegerField(null=False)
