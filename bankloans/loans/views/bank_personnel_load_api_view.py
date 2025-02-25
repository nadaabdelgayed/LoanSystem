from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from loans.models.application_status import ApplicationStatus
from loans.models.bank_balance_model import BankBalance
from loans.models.loan_application_model import LoanApplication
from loans.models.loan_model import Loan
from loans.models.transaction_model import Transaction, TransactionType
from ..serializers import  LoanApplicationSerializer


class BankPersonnelLoanApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get(self, request):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Bank Personnel"):
            loan_applications = LoanApplication.objects.filter(loan_application_status=ApplicationStatus.PENDING.value)
            serializer = LoanApplicationSerializer(loan_applications, many=True)
            return Response({'loan_applications':serializer.data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            if(request.data.get("application_status"==None or request.data.get("id")==None or request.data.get("loan_interest_rate")==None)):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'please ensure all fields are filled:':'application_status, id, loan_interest_rate'})
            bankBalance=BankBalance.objects.get(pk=1)
            appStatus=request.data.get('application_status')
            loan_application = LoanApplication.objects.get(pk=request.data.get('id'))
            if(loan_application.loan_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            loan_application.loan_application_status = appStatus
            
            
            if(loan_application.loan_application_status==ApplicationStatus.APPROVED.value):
                if(bankBalance.bank_balance<loan_application.loan_amount):
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'bank balance':'not enough'})
                bankBalance.bank_balance-=loan_application.loan_amount
                bankBalance.save()
                Loan.objects.create(loan_amount=loan_application.loan_amount,
                                    loan_user_id=loan_application.user_id,
                                    loan_interest=request.data.get('loan_interest_rate'),
                                    loan_tenure=loan_application.loan_tenure)
                Transaction.objects.create(transaction_type=TransactionType.LOAN.value,transaction_amount=loan_application.loan_amount,transaction_user_id=loan_application.user_id)
            loan_application.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request,pk):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            loan_application = LoanApplication.objects.get(pk=pk)
            if(loan_application.loan_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            loan_application.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)