from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('', views.api_root),
    path('accounts/', views.AccountList.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.AccountDetail.as_view(), name='account-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('records/', views.RecordsList.as_view(), name='records-list'),
    path('records/<int:pk>/', views.RecordsDetail.as_view(), name='records-detail'),
    path('methodofpayment/', views.MethodOfPaymentList.as_view(), name='methodofpayment-list'),
    path('methodofpayment/<int:pk>/', views.MethodOfPaymentDetail.as_view(), name='methodofpayment-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),    
]

# Using format suffixes gives us URLs that explicitly refer to a given format
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-token-auth/', views.CustomDiogenesAuthToken.as_view(), name='api_token_auth'),
]