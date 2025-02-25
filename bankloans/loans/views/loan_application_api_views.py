from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from loans.models.bank_balance_model import BankBalance
from loans.models.loan_application_model import LoanApplication
from loans.models.loan_params_model import LoanParams
from ..serializers import  LoanApplicationPostSerializer, LoanApplicationSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class LoanApplicationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        if(request.data.get('loan_amount')==None or request.data.get('loan_tenure')==None):
            return Response(status=status.HTP_400_BAD_REQUEST, data={'error':'loan_amount and loan_tenure are required'})
        data = {
            'loan_amount': request.data.get('loan_amount'),
            'loan_tenure': request.data.get('loan_tenure'),
            'user_id': request.user.id,
        }
        bank_balance = BankBalance.objects.get(id=1)
        loan_params = LoanParams.objects.get(id=1)
        if(bank_balance.bank_balance < data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Insufficient Balance, please try again later or enter an amount less than bank balance: '+str(bank_balance.bank_balance) })
        if(loan_params.bank_min_loan > data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Loan Amount is less than minimum loan amount: '+str(loan_params.bank_min_loan) })
        if(loan_params.bank_max_loan < data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Loan Amount is greater than maximum loan amount: '+str(loan_params.bank_max_loan) })
        serializer = LoanApplicationPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if(len(request.user.groups.all())==0 or(len(request.user.groups.all())>0 and request.user.groups.all()[0].name!="Customer")):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        ct=ContentType.objects.get_for_model(LoanApplication)
        loan_permission=Permission.objects.filter(content_type=ct)
        loan_applications = LoanApplication.objects.filter(user_id=request.user.id)
        serializer = LoanApplicationSerializer(loan_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request,pk):
        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        loan_application = LoanApplication.objects.get(pk=pk)
        if(loan_application.user_id != request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        loan_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
