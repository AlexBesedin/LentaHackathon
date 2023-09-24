from django.db import models
from django.core.validators import MinValueValidator
from stores.models import Store
from categories.models import Category


class Sales(models.Model):
    """Модель данных продаж по магазинам."""
    
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE, 
        related_name='store_sales',
        verbose_name='Магазин'
        )
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sku_sales',
        verbose_name='Товар'
        )
    
    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f"{self.store.store} - {self.sku.sku}"


class SalesRecord(models.Model):
    """Модель записей продаж"""
    
    fact = models.ForeignKey(
        Sales, 
        on_delete=models.CASCADE, 
        related_name='sales_records'
        )
    date = models.DateField(
        verbose_name='Дата'
        )
    sales_type = models.IntegerField(
        verbose_name='Тип продаж'
        )
    sales_units = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество единиц'
        )
    sales_units_promo = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество акционных единиц'
        )
    sales_rub = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Продажи в рублях'
        )
    sales_rub_promo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Акционные продажи в рублях'
        )
    
    class Meta:
        verbose_name = 'Запись продаж'
        verbose_name_plural = 'Записи продаж'

    def __str__(self):
        return f"{self.fact} - {self.date}"
