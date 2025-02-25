from django.db import models
from django.contrib.auth.models import User

from loans.models.application_status import ApplicationStatus


class FundApplication(models.Model):
    fund_application_id = models.AutoField(primary_key=True)
    fund_application_created = models.DateTimeField(auto_now_add=True)
    fund_application_updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fund_application_status = models.CharField(max_length=50, default=ApplicationStatus.PENDING.value,choices=[(tag.name, tag.value) for tag in ApplicationStatus])
    fund_amount = models.IntegerField()

    def __str__(self):
        return self.fund_application_status   