from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import BankDetailsSerializer, TransferSerializer
from blogpost.utils import send_normal_mail
from blogpost.models import CustomUser
from .models import BankDetails
# Create your views here.

class OpenAccount(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankDetailsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email_subject = 'Account Opening Complete'
        email_body = f'''
                        Dear {request.user.username}, \n This is to inform you that account opening has been completed\n
                        Here at Edozie Bank, we value our customers and we do our best to ensure customer satisfaction.
                        Thank you for choosing Edozie Bank. We promise an unforgettable experience.
'''

        send_normal_mail(receiver=request.user.email, subject=email_subject, body=email_body )
        return Response(
            {
                'message': 'You have successfully opened an account with us'
            }, status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        customer_id = BankDetails.objects.get(account_holder=request.user.id)
        return Response(
            {
                'username': request.user.username,
                'email_address': request.user.email,
                'account_balance': customer_id.account_balance,
                'account_number': customer_id.account_number,
                'phonenumber': customer_id.phonenumber,
            }
        )
    
class TransferView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request):
        serializer = self.serializer_class(request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Transfer Successful'
            }, status=status.HTTP_201_CREATED
        )