from rest_framework import serializers
from accounting_records.models import Account, Category, Records, MethodOfPayment
from django.contrib.auth.models import User

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #account_type = serializers.(source='get_account_type_display')
    class Meta:
        model = Account
        fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category_type = serializers.CharField(source='get_category_type_display')
    class Meta:
        model = Category
        fields = '__all__'

class RecordsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Records
        fields = '__all__'

class MethodOfPaymentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = MethodOfPayment
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    account_related = serializers.HyperlinkedRelatedField(many=True, view_name='account-detail', read_only=True)
    category_related = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)
    records_related = serializers.HyperlinkedRelatedField(many=True, view_name='records-detail', read_only=True)
    methodofpayment_related = serializers.HyperlinkedRelatedField(many=True, view_name='methodofpayment-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'account_related', 'category_related', 'records_related', 'methodofpayment_related']


   