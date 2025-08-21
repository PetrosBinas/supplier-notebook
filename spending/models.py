from django.db import models
from suppliers.models import Product, Supplier
from decimal import Decimal

class ProductSpendingMonthly(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("product", "month", "year")
    
    def save(self, *args, **kwargs):

        if self.pk is not None:

            in_product = self.product
            in_year = self.year
            in_month = self.month
            in_supplier = self.product.supplier

            old_record = ProductSpendingMonthly.objects.get(pk=self.pk)
            if old_record.cost != self.cost:
                cost_dif = self.cost - old_record.cost

                yearly_spending, _ = ProductSpendingYearly.objects.get_or_create(
                    product = in_product,
                    year = in_year,
                    defaults={"cost": Decimal("0.00")}
                )

                monthly_supplier_spending, _ = SupplierSpendingMonthly.objects.get_or_create(
                    supplier = in_supplier,
                    month = in_month,
                    year = in_year,
                    defaults={"cost": Decimal("0.00")}
                )

                yearly_supplier_spending, _ = SupplierSpendingYearly.objects.get_or_create(
                    supplier = in_supplier,
                    year = in_year,
                    defaults={"cost": Decimal("0.00")}
                )

                yearly_spending.add_to_year(cost_dif)
                monthly_supplier_spending.add_to_month(cost_dif)
                yearly_supplier_spending.add_to_year(cost_dif)
        
        super().save(**kwargs)
        


class ProductSpendingYearly(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("product", "year")

    def add_to_year(self, cost_dif):
        self.cost += cost_dif
        self.save()
        print(f"so far {self.product.name} for year {self.year} has costed {self.cost}$")



class SupplierSpendingMonthly(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("supplier", "month", "year")

    def add_to_month(self, cost_dif):
        self.cost += cost_dif
        self.save()
        print(f"so far we gave {self.supplier.name} {self.cost}$ for this month")



class SupplierSpendingYearly(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("supplier", "year")
    
    def add_to_year(self, cost_dif):
        self.cost += cost_dif
        self.save()
        print(f"so far we gave {self.supplier.name} {self.cost}$ for this year")