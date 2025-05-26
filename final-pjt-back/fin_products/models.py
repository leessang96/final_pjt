
from django.db import models

### 예금
class TermDeposit(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True)
    dcls_month = models.CharField(max_length=6)
    fin_co_no = models.CharField(max_length=20)
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=100)
    join_deny = models.CharField(max_length=2)
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    etc_note = models.TextField(blank=True, null=True)
    mtrt_int = models.TextField(blank=True, null=True)

class TermDepositOption(models.Model):
    product = models.ForeignKey(TermDeposit, related_name='optionList', on_delete=models.CASCADE)
    save_trm = models.CharField(max_length=10)
    intr_rate_type_nm = models.CharField(max_length=20)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()


### 적금
class InstallmentSaving(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True)
    dcls_month = models.CharField(max_length=6)
    fin_co_no = models.CharField(max_length=20)
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=100)
    join_deny = models.CharField(max_length=2)
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    etc_note = models.TextField(blank=True, null=True)
    mtrt_int = models.TextField(blank=True, null=True)

class InstallmentSavingOption(models.Model):
    product = models.ForeignKey(InstallmentSaving, related_name='optionList', on_delete=models.CASCADE)
    save_trm = models.CharField(max_length=10)
    intr_rate_type_nm = models.CharField(max_length=20)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
