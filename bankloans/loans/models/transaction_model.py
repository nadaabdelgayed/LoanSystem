from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class TransactionType(Enum):
    LOAN = 'loan'
    FUND = 'fund'
    INSTALLMENTS='installments'

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_created = models.DateTimeField(auto_now_add=True)
    transaction_updated = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in TransactionType])
    transaction_amount = models.IntegerField()
    transaction_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_type