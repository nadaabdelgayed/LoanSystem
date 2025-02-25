from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from loans.models.fund_application_model import FundApplication
from ..serializers import  FundApplicationPostSerializer, FundApplicationSerializer

class FundApplicationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if(request.user.groups.all()[0].name=="Loan Provider"):
            if(request.data.get('fund_amount')==None):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'fund_amount is required'})
            data = {
            'fund_amount': request.data.get('fund_amount'),
            'user_id': request.user.id,
            }
            serializer = FundApplicationPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def get(self, request):
        fund_applications = FundApplication.objects.filter(user_id=request.user.id)
        serializer = FundApplicationSerializer(fund_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request,pk):
        fund_application = FundApplication.objects.get(pk=pk)
        if(fund_application.user_id != request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        fund_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
