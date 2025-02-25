from django.db import models
    
class BankBalance(models.Model):
    bank_balance = models.IntegerField()