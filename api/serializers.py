from rest_framework import serializers
from accounting_records.models import Account, Category, Records, MethodOfPayment

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'

class MethodOfPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodOfPayment
        fields = '__all__'


   