from django.db import models
from django.contrib.auth.models import AbstractUser
from fin_products.models import TermDeposit, InstallmentSaving

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    age = models.PositiveIntegerField(blank=True, null=True)
    salary = models.BigIntegerField(blank=True, default=0)
    current_amount = models.BigIntegerField(blank=True, default=0)
   #  sub_product = models.JSONField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    pass


 # 가입한 상품 필드 추가
    joined_term_products = models.ManyToManyField(TermDeposit, blank=True)
    joined_saving_products = models.ManyToManyField(InstallmentSaving, blank=True)