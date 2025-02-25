from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from loans.models.application_status import ApplicationStatus
from loans.models.bank_balance_model import BankBalance
from loans.models.fund_application_model import FundApplication
from loans.models.transaction_model import Transaction, TransactionType
from ..serializers import  FundApplicationSerializer

class BankPersonnelFundApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Bank Personnel"):
            fund_applications = FundApplication.objects.filter(fund_application_status=ApplicationStatus.PENDING.value)
            fund_serializer = FundApplicationSerializer(fund_applications, many=True)
            return Response({'fund_applications':fund_serializer.data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            if(request.data.get("application_status"==None or request.data.get("id")==None)):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'please ensure all fields are filled:':'application_status, id'})
            bankBalance=BankBalance.objects.get(pk=1)
            appStatus=request.data.get('application_status')
            fund_application = FundApplication.objects.get(pk=request.data.get('id'))
            if(fund_application.fund_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'application status':'not pending'})
            fund_application.fund_application_status = appStatus
            if(fund_application.fund_application_status==ApplicationStatus.APPROVED.value):
                bankBalance.bank_balance+=fund_application.fund_amount
                Transaction.objects.create(transaction_type=TransactionType.FUND.value,transaction_amount=fund_application.fund_amount,transaction_user_id=fund_application.user_id)
                bankBalance.save()
            fund_application.save()
                    

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request,pk):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            fund_application = FundApplication.objects.get(pk=pk)
            if(fund_application.fund_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fund_application.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    