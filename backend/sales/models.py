from django.db import models
from django.core.validators import MinValueValidator
from stores.models import Store
from categories.models import Category


class Sales(models.Model):
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE, 
        related_name='store_sales'
        )
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sku_sales'
        )

    def __str__(self):
        return f"{self.store.store} - {self.sku.sku}"


class SalesRecord(models.Model):
    fact = models.ForeignKey(
        Sales, 
        on_delete=models.CASCADE, 
        related_name='sales_records')
    date = models.DateField()
    sales_type = models.IntegerField()
    sales_units = models.IntegerField(
        validators=[MinValueValidator(0)]
        )
    sales_units_promo = models.IntegerField(
        validators=[MinValueValidator(0)]
        )
    sales_rub = models.DecimalField(
        max_digits=10, 
        decimal_places=2
        )
    sales_rub_promo = models.DecimalField(
        max_digits=10, 
        decimal_places=2
        )

    def __str__(self):
        return f"{self.fact} - {self.date}"
