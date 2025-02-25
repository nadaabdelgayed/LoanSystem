# from django.conf.urls import url
from django.urls import path, include

from loans.views.amortization_api_view import AmortizationApiView
from loans.views.bank_personnel_fund_api_view import BankPersonnelFundApiView
from loans.views.bank_personnel_load_api_view import BankPersonnelLoanApiView
from loans.views.fund_application_api_view import FundApplicationApiView
from loans.views.loan_application_api_views import LoanApplicationApiView
from loans.views.transaction_api_view import TransactionApiView

urlpatterns = [
    path('loan-application/', LoanApplicationApiView.as_view()),
    path('loan-application/<int:pk>/', LoanApplicationApiView.as_view()),
    path('transaction/', TransactionApiView.as_view()),
    path('fund-application/', FundApplicationApiView.as_view()),
    path('fund-application/<int:pk>/', FundApplicationApiView.as_view()),
    path('bank-panel-fund/', BankPersonnelFundApiView.as_view()),
    path('bank-panel/<int:pk>/', BankPersonnelFundApiView.as_view()),
    path('bank-panel-loan/', BankPersonnelLoanApiView.as_view()),
    path('bank-panel-loan/<int:pk>/', BankPersonnelLoanApiView.as_view()),
    path('amortization/<int:pk>/',  AmortizationApiView.as_view()),
]