from django.db import models


class Category(models.Model):
    """Класс Категории."""

    sku = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    uom = models.PositiveIntegerField()

    def __str__(self):
        return self.sku
