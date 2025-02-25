from django.db import models
from django.contrib.auth.models import User

from loans.models.application_status import ApplicationStatus

class LoanApplication(models.Model):
    loan_application_id = models.AutoField(primary_key=True)
    loan_application_created = models.DateTimeField(auto_now_add=True)
    loan_application_updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_application_status = models.CharField(max_length=50, default=ApplicationStatus.PENDING.value,choices=[(tag.name, tag.value) for tag in ApplicationStatus])
    loan_amount = models.IntegerField()
    loan_tenure = models.IntegerField()

    def __str__(self):
        return self.loan_application_status  