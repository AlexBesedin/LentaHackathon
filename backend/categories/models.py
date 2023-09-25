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
        related_name='groups'
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
        related_name='categories'
    )

    class Meta:
        verbose_name = "Субкатегория"
        verbose_name_plural = "Субкатегории"
        # ordering = ("category",)

    def __str__(self):
        return self.category


class Category(models.Model):
    """Класс Категории продуктов."""

    sku = models.CharField(
        max_length=50,
        verbose_name='захэшированное id товара',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    category = models.ForeignKey(
        CategoryProduct,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='subcategories'
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
