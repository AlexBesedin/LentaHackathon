from django.db import models


class Store(models.Model):
    """Класс магазин."""

    store = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    type_format = models.IntegerField()
    loc = models.IntegerField()
    size = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.store
