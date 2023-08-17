from django.test import TestCase
import json
from django.contrib.auth.models import User
from accounting_records.models import Account


# Create your tests here.

#create a test for obtain token
class ObtainTokenTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'admintest',
            'password': 'admintest',
        }
        User.objects.create_user(**self.credentials)

    def test_obtain_token(self):
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('username' in response.data)
        
    def test_obtain_token_wrong_password(self):
        self.credentials['password'] = 'wrong'
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)
        self.assertTrue(response.status_code, 400)
        self.assertTrue('non_field_errors' in response.data)
        self.assertTrue('Unable to log in with provided credentials.' in response.data['non_field_errors'])

    def test_obtain_token_wrong_username(self):
        self.credentials['username'] = 'wrong'
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('non_field_errors' in response.data)
        self.assertTrue('Unable to log in with provided credentials.' in response.data['non_field_errors'])

    def test_obtain_token_wrong_username_and_password(self):
        self.credentials['username'] = 'wrong'
        self.credentials['password'] = 'wrong'
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('non_field_errors' in response.data)
        self.assertTrue('Unable to log in with provided credentials.' in response.data['non_field_errors'])

    def test_obtain_token_empty_username(self):
        self.credentials['username'] = ''
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('username' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['username'])
    
    def test_obtain_token_empty_password(self):
        self.credentials['password'] = ''
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('password' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['password'])
    
    def test_obtain_token_empty_username_and_password(self):
        self.credentials['username'] = ''
        self.credentials['password'] = ''
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('username' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['username'])
        self.assertTrue('password' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['password'])

    def test_obtain_token_wrong_username_and_empty_password(self):
        self.credentials['username'] = 'wrong'
        self.credentials['password'] = ''
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('password' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['password'])

    def test_obtain_token_empty_username_and_wrong_password(self):
        self.credentials['username'] = ''
        self.credentials['password'] = 'wrong'
        response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)        
        self.assertTrue(response.status_code, 400)
        self.assertTrue('username' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['username'])

class APIAccountTest(TestCase):    

    def setUp(self):
        self.credentials = {
            'username': 'admintest',
            'password': 'admintest',
        }
        User.objects.create_user(**self.credentials)
        self.user = User.objects.get(username='admintest')
        self.response = self.client.post('/api/api-token-auth/', self.credentials, follow=True)
        Account.objects.create(name="test", amount=1000, owner=self.user)
    
    def test_get_account_with_token(self):
        token = self.response.data['token']
        response = self.client.get('/api/accounts/', HTTP_AUTHORIZATION='Token ' + token)        
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.data), 1)
        self.assertTrue(response.data['results'][0]['name'], 'test')
        self.assertTrue(response.data['results'][0]['amount'], 1000)
        self.assertTrue(response.data['results'][0]['owner'], self.user.id)

    def test_get_account_without_token(self):
        response = self.client.get('/api/accounts/')        
        self.assertTrue(response.status_code, 401)
        self.assertTrue('detail' in response.data)
        self.assertTrue('Authentication credentials were not provided.' in response.data['detail'])

    def test_get_account_with_wrong_token(self):
        response = self.client.get('/api/accounts/', HTTP_AUTHORIZATION='Token ' + 'wrong')        
        self.assertTrue(response.status_code, 401)
        self.assertTrue('detail' in response.data)
        self.assertTrue('Invalid token.' in response.data['detail'])
    
    def test_create_account_with_token(self):
        token = self.response.data['token']
        data = {
            'name': 'test2',
            'amount': 1000,
            'owner': self.user.id
        }
        response = self.client.post('/api/accounts/', data, HTTP_AUTHORIZATION='Token ' + token, format='json')        
        self.assertTrue(response.status_code, 201)
        self.assertTrue(response.data['name'], 'test2')
        self.assertTrue(response.data['amount'], 1000)
        self.assertTrue(response.data['owner'], self.user.id)
    
    def test_create_account_without_token(self):
        data = {
            'name': 'test2',
            'amount': 1000,
            'owner': self.user.id
        }
        response = self.client.post('/api/accounts/', data, format='json')        
        self.assertTrue(response.status_code, 401)
        self.assertTrue('detail' in response.data)
        self.assertTrue('Authentication credentials were not provided.' in response.data['detail'])

    def test_create_account_with_wrong_token(self):
        response = self.client.post('/api/accounts/', HTTP_AUTHORIZATION='Token ' + 'wrong')
        self.assertTrue(response.status_code, 401)
        self.assertTrue('detail' in response.data)
        self.assertTrue('Invalid token.' in response.data['detail'])
    
    def test_create_account_with_wrong_data(self):
        token = self.response.data['token']
        data = {
            'name': '',
            'amount': 1000,
            'owner': self.user.id
        }
        response = self.client.post('/api/accounts/', data, HTTP_AUTHORIZATION='Token ' + token, format='json')
        self.assertTrue(response.status_code, 400)
        self.assertTrue('name' in response.data)
        self.assertTrue('This field may not be blank.' in response.data['name'])


      
        
        
    