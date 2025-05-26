from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    age = models.PositiveIntegerField(blank=True, null=True)
    salary = models.BigIntegerField(blank=True, default=0)
    current_amount = models.BigIntegerField(blank=True, default=0)
    sub_product = models.JSONField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    pass