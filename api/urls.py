from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('accounts/', views.account_list),
    path('accounts/<int:pk>/', views.account_detail),
]

# Using format suffixes gives us URLs that explicitly refer to a given format
urlpatterns = format_suffix_patterns(urlpatterns)