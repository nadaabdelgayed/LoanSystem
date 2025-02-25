from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from loans.models.loan_model import Loan

    
class AmortizationApiView(APIView):
    # only loan providers can access this class
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request,pk):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Loan Provider"):
            loan = Loan.objects.filter(loan_id=pk)
            if(len(loan)==0):
                return Response(status=status.HTTP_404_NOT_FOUND)
            loan=loan[0]
            AmortizationTable=[]
            for i in range(loan.loan_tenure):
                entry={
                    'month':i+1,
                    'payment':'{:.2f}'.format(loan.loan_amount/loan.loan_tenure+loan.loan_interest*loan.loan_amount/loan.loan_tenure),
                    'principal':loan.loan_amount/loan.loan_tenure,
                    'interest':loan.loan_interest*loan.loan_amount/loan.loan_tenure,
                    'balance':loan.loan_amount-(i+1)*loan.loan_amount/loan.loan_tenure,
                }
                AmortizationTable.append(entry)
            return Response({'amortization_table':AmortizationTable}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
