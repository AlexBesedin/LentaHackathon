from django.db import models


class Store(models.Model):
    """Класс магазин."""

    store = models.CharField(
        max_length=50,
        verbose_name='захэшированное id магазина',
    )
    city = models.CharField(
        max_length=50,
        verbose_name='захэшированное id города',
    )
    division = models.CharField(
        max_length=50,
        verbose_name='захэшированное id дивизиона',
    )
    type_format = models.IntegerField(
        verbose_name='id формата магазина',
    )
    loc = models.IntegerField(
        verbose_name='id тип локации/окружения магазина',
    )
    size = models.IntegerField(
        verbose_name='id типа размера магазина',
    )
    is_active = models.BooleanField(
        verbose_name='флаг активного магазина на данный момент',
    )

    class Meta:
        ordering = ('store',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.store
