from django.contrib import admin
from .models import Account, Category, Records, MethodOfPayment
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Records)
admin.site.register(MethodOfPayment)
admin.site.register(Account)