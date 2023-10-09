from django.db import models


class Group(models.Model):
    """Класс Группа продуктовой иерархии."""

    group = models.CharField(
        max_length=50,
        verbose_name='захэшированная группа товара',
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("group",)

    def __str__(self):
        return self.group


class CategoryProduct(models.Model):
    """Класс Категория продуктовой иерархии."""

    category = models.CharField(
        max_length=50,
        verbose_name='захэшированная категория товара',
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name='захэшированная группа товара',
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("category",)

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    """Класс субкатегорий продуктовой иерархии."""

    subcategory = models.CharField(
        max_length=50,
        verbose_name='захэшированная подкатегория товара',
    )

    category = models.ForeignKey(
        CategoryProduct,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='захэшированная категория товара',
    )

    class Meta:
        verbose_name = "Субкатегория"
        verbose_name_plural = "Субкатегории"
        ordering = ("subcategory",)

    def __str__(self):
        return self.subcategory


class Category(models.Model):
    """Класс Категории продуктов."""
    UOM_CHOICES = [
        (1, 'Шт.'),
        (17, 'кг/г'),
        ]

    sku = models.CharField(
        max_length=50,
        verbose_name='захэшированное id товара',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='main_groups',
        verbose_name='захэшированная группа товара',
    )
    category = models.ForeignKey(
        CategoryProduct,
        on_delete=models.CASCADE,
        related_name='main_categories',
        verbose_name='захэшированная категория товара',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='main_subcategories',
        verbose_name='захэшированная подкатегория товара',
    )
    uom = models.IntegerField(
        choices=UOM_CHOICES,
        verbose_name='маркер, обозначающий продаётся товар на вес или в ШТ',
    )

    class Meta:
        ordering = (
            'group',
            'category',
            'subcategory',
            'sku',
        )
        verbose_name = 'Свобная таблица категории'
        verbose_name_plural = 'Свобная таблица категорий'

    def __str__(self):
        return self.sku

    def get_uom_display(self):
        if self.uom == 1:
            return 'шт'
        elif self.uom == 17:
            return 'кг'
        else:
            return 'Неизвестно'
