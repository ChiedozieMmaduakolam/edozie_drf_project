from rest_framework import serializers
from .models import BankDetails, Transer
from rest_framework.exceptions import ValidationError

class BankDetailsSerializer(serializers.ModelSerializer):
    phonenumber = serializers.CharField(min_length=8, max_length=20)
    
    class Meta:
        model = BankDetails
        exclude = ['account_holder']

    def validate(self, attrs):
        phone_from_db = BankDetails.objects.filter(phonenumber=attrs['phonenumber']).first()
        if phone_from_db:
            raise serializers.ValidationError('Phonenumber already exists. Please use a different one')
        if len(attrs['phonenumber']) < 8 or len(attrs['phonenumber']) > 20:
            raise serializers.ValidationError('Phonenumber must be greater than 8 characters and less than or equal to 20 characters')
        return attrs
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        bank_details = BankDetails.objects.create(account_holder=user, **validated_data)
        account_number = bank_details.phonenumber[-10:]
        bank_details.account_number = account_number
        bank_details.save()
        return bank_details
    

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transer
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        inputted_account_number = BankDetails.objects.filter(account_number=attrs['receiver_account']).first()
        if not inputted_account_number:
            raise serializers.ValidationError('Invalid account number provided'.title())
        inputted_amount = attrs['amount']
        sender_balance = BankDetails.objects.get(account_holder=request.user.id).account_balance
        if inputted_amount > sender_balance:
            raise serializers.ValidationError('Insufficient funds'.title())
        if inputted_amount <= 0:
            raise serializers.ValidationError('Transfer amount must not be less than 10 pounds')
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        sender_balance = BankDetails.objects.get(account_holder=request.user.id).account_balance
        receiver = BankDetails.objects.get(account_number=validated_data['receiver_account'])
        receiver_balance = receiver.account_balance
        sender_balance = sender_balance - validated_data['amount']
        receiver_balance = receiver_balance + validated_data['amount']
        transfer_details = Transer.objects.create(
            sender = request.user.id,
            receiver_account = validated_data['receiver_account'],
            amount = validated_data['amount'],
            date = validated_data['date'], 
            narration = validated_data['narration']
        )
        transfer_details.save()