from django.shortcuts import render
from .models import Category

# Create your views here.

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})