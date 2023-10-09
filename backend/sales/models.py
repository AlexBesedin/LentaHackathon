from django.contrib.auth import get_user_model
from django.db import models

from categories.models import Category
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


class UserSalesBookmark(models.Model):
    """Модель закладок пользователя для сохранения данных по продажам."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='sales_bookmarks',
        verbose_name='Пользователь',
        )
    sales = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name='sales_bookmarked_by',
        verbose_name='Прогноз магазина',
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
        )

    class Meta:
        verbose_name = 'Закладка пользователя по данным продаж.'
        verbose_name_plural = 'Закладки пользователя по данным продаж.'
        unique_together = [['user', 'sales', ]]

    def __str__(self):
        return f"{self.user} - {self.sales}"
