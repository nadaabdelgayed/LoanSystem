from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class LoanStatus(Enum):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    loan_created = models.DateTimeField(auto_now_add=True)
    loan_updated = models.DateTimeField(auto_now=True)
    loan_amount = models.IntegerField()
    loan_tenure = models.IntegerField()
    loan_interest = models.FloatField()
    loan_status = models.CharField(max_length=50, default=LoanStatus.ONGOING.value,choices=[(tag.name, tag.value) for tag in LoanStatus])
    loan_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.loan_status
    