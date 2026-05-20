from django.db import models
from blogpost.models import CustomUser
from django.utils import timezone
# Create your models here.



class BankDetails(models.Model):
    account_holder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_balance = models.FloatField(default=10000.00)
    phonenumber = models.CharField(max_length=20, unique=True)
    account_number = models.CharField(max_length=11,default=False, unique=True)


class Transer(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver_account = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateTimeField(timezone.now())
    narration = models.CharField(max_length=2000,default=False)