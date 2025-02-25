from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from loans.models.bank_balance_model import BankBalance
from loans.models.loan_model import Loan
from loans.models.transaction_model import Transaction, TransactionType
from ..serializers import  TransactionSerializer

class TransactionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        transactions = Transaction.objects.filter(transaction_user_id=request.user.id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        if(request.data.get('transaction_amount')==None):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Invalid data, please ensure that you have entered transaction_type and transaction_amount'})
        loans= Loan.objects.filter(loan_user_id=request.user.id)
        if(len(loans)==0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'No loans found'})
        count=0
        for loan in loans:
            if(loan.loan_status=="ongoing"):
                count+=1
        if(count==0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'No ongoing loans found'})  
        data = {
            'transaction_type': TransactionType.INSTALLMENTS.value,
            'transaction_amount': request.data.get('transaction_amount'),
            'transaction_user_id': request.user,
        }
        bankBal=BankBalance.objects.get(pk=1)
        bankBal.bank_balance+=request.data.get('transaction_amount')
        bankBal.save()
        Transaction.objects.create(**data)
        return Response(status=status.HTTP_201_CREATED)