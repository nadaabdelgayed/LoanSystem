from django.test import TestCase

from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from loans.models.application_status import ApplicationStatus
from loans.models.bank_balance_model import BankBalance
from loans.models.fund_application_model import FundApplication
from loans.models.transaction_model import Transaction
from loans.models.loan_application_model import LoanApplication

class BankPersonnelFundApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='nadabank', password='nada1234')
        self.admin_group = Group.objects.create(name='Bank Personnel')
        self.user.groups.add(self.admin_group)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)
        self.bank_balance = BankBalance.objects.create(bank_balance=1000)
        self.fund_application = FundApplication.objects.create(
            user_id=self.user,
            fund_amount=500,
            fund_application_status=ApplicationStatus.PENDING.value
        )        
        

    def test_get_fund_applications(self):
        response = self.client.get('/bank-panel-fund/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fund_applications', response.data)

    def test_post_approve_fund_application(self):
        data = {'application_status': ApplicationStatus.APPROVED.value, 'id': self.fund_application.fund_application_id}
        response = self.client.post('/bank-panel-fund/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.fund_application.refresh_from_db()
        self.assertEqual(self.fund_application.fund_application_status, ApplicationStatus.APPROVED.value)
        self.bank_balance.refresh_from_db()
        self.assertEqual(self.bank_balance.bank_balance, 1500)


class BankPersonnelLoanApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bankstaff', password='password123')
        self.admin_group = Group.objects.create(name='Bank Personnel')
        self.user.groups.add(self.admin_group)
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)
        self.bank_balance = BankBalance.objects.create(bank_balance=5000)
        self.loan_application = LoanApplication.objects.create(
            user_id=self.user,
            loan_amount=1000,
            loan_tenure=12,
            loan_application_status=ApplicationStatus.PENDING.value
        )

    def test_get_loan_applications(self):
        response = self.client.get('/bank-panel-loan/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('loan_applications', response.data)

    def test_post_approve_loan_application(self):
        data = {
            'application_status': ApplicationStatus.APPROVED.value,
            'id': self.loan_application.loan_application_id,
            'loan_interest_rate': 5.5
        }
        response = self.client.post('/bank-panel-loan/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan_application.refresh_from_db()
        self.assertEqual(self.loan_application.loan_application_status, ApplicationStatus.APPROVED.value)
        self.bank_balance.refresh_from_db()
        self.assertEqual(self.bank_balance.bank_balance, 4000)  # 5000 - 1000 loan amount

    def test_post_reject_loan_application(self):
        data = {
            'application_status': ApplicationStatus.REJECTED.value,
            'id': self.loan_application.loan_application_id,
            'loan_interest_rate': 5.5
        }
        response = self.client.post('/bank-panel-loan/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan_application.refresh_from_db()
        self.assertEqual(self.loan_application.loan_application_status, ApplicationStatus.REJECTED.value)
        self.bank_balance.refresh_from_db()
        self.assertEqual(self.bank_balance.bank_balance, 5000)  # No change since loan is rejected

    def test_post_insufficient_bank_balance(self):
        self.bank_balance.bank_balance = 500  # Less than loan amount
        self.bank_balance.save()
        data = {
            'application_status': ApplicationStatus.APPROVED.value,
            'id': self.loan_application.loan_application_id,
            'loan_interest_rate': 5.5
        }
        response = self.client.post('/bank-panel-loan/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('bank balance', response.data)

    def test_delete_loan_application(self):
        response = self.client.delete(f'/bank-panel-loan/{self.loan_application.loan_application_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(LoanApplication.DoesNotExist):
            LoanApplication.objects.get(pk=self.loan_application.loan_application_id)

    def test_delete_non_pending_loan_application(self):
        self.loan_application.loan_application_status = ApplicationStatus.APPROVED.value
        self.loan_application.save()
        response = self.client.delete(f'/bank-panel-loan/{self.loan_application.loan_application_id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
