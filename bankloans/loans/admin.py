from django.contrib import admin

from loans.models.bank_balance_model import BankBalance
from loans.models.fund_application_model import FundApplication
from loans.models.loan_application_model import LoanApplication
from loans.models.loan_model import Loan
from loans.models.loan_params_model import LoanParams
from loans.models.transaction_model import Transaction

# Register your models here.

# admin.site.register(User)
admin.site.register(Loan)
admin.site.register(LoanApplication)
admin.site.register(Transaction)
admin.site.register(FundApplication)
admin.site.register(LoanParams)

admin.site.register(BankBalance)
