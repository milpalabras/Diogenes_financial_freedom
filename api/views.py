from rest_framework import generics
from rest_framework import mixins
from accounting_records.models import Account, Category, Records, MethodOfPayment
from api.serializers import AccountSerializer, CategorySerializer, RecordsSerializer, MethodOfPaymentSerializer

# Create your views here.

#views for accounts model

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


#views for category model

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#views for records model

class RecordsList(generics.ListCreateAPIView):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer

class RecordsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer

#views for method of payment model

class MethodOfPaymentList(generics.ListCreateAPIView):
    queryset = MethodOfPayment.objects.all()
    serializer_class = MethodOfPaymentSerializer

class MethodOfPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MethodOfPayment.objects.all()
    serializer_class = MethodOfPaymentSerializer

