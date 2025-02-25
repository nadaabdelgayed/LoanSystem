from django.db import models

class LoanParams(models.Model):
    bank_min_loan = models.IntegerField()
    bank_max_loan = models.IntegerField()