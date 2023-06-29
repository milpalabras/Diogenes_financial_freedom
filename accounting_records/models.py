from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Account(models.Model):
    '''Account model for save the accounts of the user'''
    owner = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    class AccountType (models.TextChoices):
        GENERAL = 'GRAL', _('General')
        EFECTIVO ='EFEC', _('Efectivo')
        BANCARIA = 'BANC', _('Cuenta Bancaria')
        CREDITO = 'CRED', _('Tarjeta de Credito')
        AHORRO = 'AHOR', _('Cuenta de ahorros')
        EXTRA = 'EXTR', _('Extra')
        SEGURO = 'SEGU', _('Seguro')
        INVERSION = 'INVE', _('Inversión')
        PRESTAMO = 'PRES', _('Prestamo')
        HIPOTECA = 'HIPO', _('Hipoteca')
        OTRO = 'OTRO', _('Otro')
    account_type = models.CharField(max_length=4, choices=AccountType.choices, default=AccountType.GENERAL)
    amount = models.DecimalField(max_digits=50, decimal_places=2, validators=[MinValueValidator(0.00)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Category(MPTTModel):
    '''Category model for save the categories of the user'''
    owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', related_query_name='subcategorie')
    class CategoryType (models.TextChoices):
        FIJO ='F', _('Gasto Fijo(Obligatorio)')
        NECESIDAD = 'N', _('Gasto Necesario(Sobrevivencia)')
        PRESCINDIBLE = 'P',_('Gasto Prescindible(Lujo)')
        INGRESO = 'I',_('Ingreso de dinero')
        PADRE = 'C',_('Categoria Padre (admin)')       

    category_type = models.CharField(max_length=1, choices=CategoryType.choices, default=CategoryType.FIJO)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by=['name']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Category'
    verbose_name_plural = 'Categories'

    def get_parent(self):
        return self.parent
    
    def get_children(self):
        return self.children.all()
    
    def get_all_children(self):
        return self.get_descendants(include_self=True)
    
    def get_all_children_id(self):
        return self.get_descendants(include_self=True).values_list('id', flat=True)
    
class Records(models.Model):
    '''Records model for save the records of income and expense by user'''
    owner = models.ForeignKey(User,related_name='records', on_delete=models.CASCADE)
    class RecordType (models.TextChoices):
        GASTO = 'GAST', _('Gasto')
        INGRESO ='INGR', _('Ingreso')
        TRANSFERENCIA = 'TRAN', _('Transferencia')
    record_type = models.CharField(max_length=4, choices=RecordType.choices, default=RecordType.GASTO)
    amount = models.DecimalField(max_digits=15,  decimal_places=2, validators=[MinValueValidator(('0.01'))])
    note = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField()
    category_id = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    account_id = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True)
    method_of_payment_id = models.ForeignKey('MethodOfPayment', on_delete=models.CASCADE, null=True, blank=True)    
    voucher = models.FileField(upload_to='vouchers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "Registros"
        verbose_name = "Registro"
        ordering = ['payment_date']

    def save(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)        
        if self.record_type == 'GAST':
            account.amount -= self.amount
        elif self.record_type == 'INGR':
            account.amount += self.amount
        account.save()
        super(Records, self).save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)        
        if self.record_type == 'GAST':
            account.amount += self.amount
        elif self.record_type == 'INGR':
            account.amount -= self.amount
        account.save()
        super(Records, self).delete(*args, **kwargs)
    
    
    def update(self, *args, **kwargs):
        account= Account.objects.get(id=self.account_id.id)
        old_amount = Records.objects.get(id=self.id).amount

        if self.record_type == 'GAST':
            if old_amount > self.amount:
                account.amount += old_amount - self.amount
            elif old_amount < self.amount:
                account.amount -= self.amount - old_amount
        elif self.record_type == 'INGR':
            if old_amount > self.amount:
                account.amount -= old_amount - self.amount
            elif old_amount < self.amount:
                account.amount += self.amount - old_amount
        account.save()
        super(Records, self).update(*args, **kwargs)
            
    def __str__(self):
        return self.get_record_type_display() + " - " + str(self.amount) + " - " + str(self.payment_date)
    
    @property
    def get_comprobante(self):
        return self.voucher.url

    
    @staticmethod
    def get_total_records_by_month(owner, month, year):
        records = Records.objects.filter(owner=owner, payment_date__month=month, payment_date__year=year)
        total_expenses = 0
        total_incomes = 0
        for record in records:
            if record.record_type == 'GAST':
                total_expenses += record.amount
            elif record.record_type == 'INGR':
                total_incomes += record.amount
        return total_expenses, total_incomes

   
    @staticmethod
    def get_total_records_by_month_and_category(owner, month, year):
        records = Records.objects.filter(owner=owner, payment_date__month=month, payment_date__year=year)
        categories = Category.objects.filter(owner=owner)
        total_expenses = []
        total_incomes = []
        for category in categories:
            total_expenses.append(0)
            total_incomes.append(0)
            for record in records:
                if record.category_id == category:
                    if record.record_type == 'GAST':
                        total_expenses[-1] += record.amount
                    elif record.record_type == 'INGR':
                        total_incomes[-1] += record.amount
        return total_expenses, total_incomes

class MethodOfPayment (models.Model):
    '''Method of payment model for save the methods of payment of the user'''
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural="Forma de pagos"
        verbose_name="Forma de pago"        

    def __str__(self):
        return self.name
    
    
   
 


