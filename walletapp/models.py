from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    full_name = models.CharField(max_length = 50)
    user = models.OneToOneField(User, on_delete= models.DO_NOTHING)


class Wallet(models.Model):
    account = models.OneToOneField(Account, on_delete=models.DO_NOTHING)
    balance = models.DecimalField(max_digits = 20, decimal_places=3)
    status = models.BooleanField(default=False)


class Transcation(models.Model):
    TRANSACTION_CHOICES = (
        ('Deposit', 'deposit'),
        ('Withdraw', 'withdraw')
    )
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_CHOICES)
    transaction_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits = 20, decimal_places=3)
