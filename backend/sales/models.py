from categories.models import Category
from django.db import models
from stores.models import Store


class SalesRecord(models.Model):
    """Модель записей продаж"""
    date = models.DateField(
        verbose_name='Дата'
        )
    sales_type = models.IntegerField(
        verbose_name='Флаг наличия промо'
        )
    sales_units = models.IntegerField(
        verbose_name='Число проданных товаров без признака промо'
        )
    sales_units_promo = models.IntegerField(
        verbose_name='Число проданных товаров с признаком промо'
        )
    sales_rub = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Продажи без признака промо в РУБ'
        )
    sales_rub_promo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Продажи с признаком промо в РУБ;'
        )

    class Meta:
        verbose_name = 'Запись продаж'
        verbose_name_plural = 'Записи продаж'

    def __str__(self):
        return f"{self.date}, {self.sales_rub_promo}"


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
    facts = models.ManyToManyField(
        SalesRecord, 
        related_name='sales_records', 
        verbose_name='Записи продаж'
        )

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f"{self.store} - {self.sku}"