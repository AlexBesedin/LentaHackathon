from django.db import models
from django.core.validators import MinValueValidator
from stores.models import Store


class Sales(models.Model):
    """Модель данных продаж по магазинам."""
    
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE, 
        related_name='store_sales',
        verbose_name='захэшированное id магазина'
        )
    sku = models.ForeignKey(
        'categories.Category', 
        on_delete=models.CASCADE, 
        related_name='sku_sales',
        verbose_name='захэшированное id товара'
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
        verbose_name='флаг наличия промо'
        )
    sales_units = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='число проданных товаров без признака промо'
        )
    sales_units_promo = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='число проданных товаров с признаком промо'
        )
    sales_rub = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='продажи без признака промо в РУБ'
        )
    sales_rub_promo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='продажи с признаком промо в РУБ;'
        )
    
    class Meta:
        verbose_name = 'Запись продаж'
        verbose_name_plural = 'Записи продаж'

    def __str__(self):
        return f"{self.fact} - {self.date}"
