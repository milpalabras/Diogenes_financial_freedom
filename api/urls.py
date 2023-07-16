from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:pk>/', views.AccountDetail.as_view()),
]

# Using format suffixes gives us URLs that explicitly refer to a given format
urlpatterns = format_suffix_patterns(urlpatterns)