from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounting_records.models import Account, Category, Records, MethodOfPayment
from api.serializers import AccountSerializer, CategorySerializer, RecordsSerializer, MethodOfPaymentSerializer

# Create your views here.

#views for accounts model

@api_view(['GET', 'POST'])
def account_list(request, format=None):
    """
    List all accounts, or create a new account using POST method.
    """
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, pk, format=None):
    '''
    Retrieve, update or delete an account.
    '''
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    