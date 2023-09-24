from django.db import models


class Category(models.Model):
    """Класс Категории продуктов."""

    sku = models.CharField(
        max_length=50,
        verbose_name='захэшированное id товара',
    )
    group = models.CharField(
        max_length=50,
        verbose_name='захэшированная группа товара',
    )
    category = models.CharField(
        max_length=50,
        verbose_name='захэшированная категория товара',
    )
    subcategory = models.CharField(
        max_length=50,
        verbose_name='захэшированная подкатегория товара',
    )
    uom = models.PositiveIntegerField(
        verbose_name='маркер, обозначающий продаётся товар на вес или в ШТ',
    )

    class Meta:
        ordering = (
            'group',
            'category',
            'subcategory',
            'sku',
        )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.group
