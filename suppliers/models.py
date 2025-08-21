from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from decimal import Decimal
import datetime


now = datetime.datetime.now()
month = now.month
year = now.year

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)

    contact_info = models.CharField(max_length=200)

    COMMUNICATION_CHOICES = [
        ('viber','Viber'),
        ('whatsapp','WhatsApp'),
        ('email','Email'),
    ]

    preferred_method = models.CharField(max_length=20, choices=COMMUNICATION_CHOICES)

    WEEKDAY_CHOICES = [
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
    ]
   
    order_days = MultiSelectField(choices=WEEKDAY_CHOICES, max_length=100, default=["Monday"])
    order_time = models.TimeField(default=datetime.time(0, 0))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            from spending.models  import SupplierSpendingMonthly, SupplierSpendingYearly
            monthly_supplier_spending, _ = SupplierSpendingMonthly.objects.get_or_create(
                supplier = self,
                month = month,
                year = year,
                defaults = {"cost": Decimal("0.00")}
            )
            monthly_supplier_spending.save()

            yearly_supplier_spending, _ = SupplierSpendingYearly.objects.get_or_create(
                supplier = self,
                year = year,
                defaults = {"cost": Decimal("0.00")}
            )
            yearly_supplier_spending.save()            



class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)

    UNIT_CHOICES = [
        ('Pieces','Pieces'),
        ('Boxes','Boxes'),
        ('kg','kg'),
        ('g','g'),
    ]

    unit = models.CharField(choices=UNIT_CHOICES, max_length=100, default='Pieces')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            from spending.models  import ProductSpendingMonthly, ProductSpendingYearly
            monthly_spending, _ = ProductSpendingMonthly.objects.get_or_create(
                product = self,
                month = month,
                year = year,
                defaults={"cost": Decimal("0.00")}
            )
            monthly_spending.save()

            yearly_spending, _ = ProductSpendingYearly.objects.get_or_create(
                product = self,
                year = year,
                defaults={"cost": Decimal("0.00")}
            )
            yearly_spending.save()


class NoteBookEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)



