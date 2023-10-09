from django.db import models


class StoreID(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='захэшированное id магазина',
    )

    class Meta:
        verbose_name = 'ID магазина'
        verbose_name_plural = 'ID магазинов'

    def __str__(self):
        return str(self.title)


class Store(models.Model):
    """Сводная таблица магазинов продуктовой иерархии."""

    STORE_CHOICES = [(0, 'НЕТ'), (1, 'ДА')]

    store = models.ForeignKey(
        StoreID,
        on_delete=models.CASCADE,
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
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='флаг активного магазина на данный момент',
        choices=STORE_CHOICES,
    )

    class Meta:
        ordering = ('store',)
        verbose_name = 'Сводная таблица магазина'
        verbose_name_plural = 'Сводная таблица магазинов'

    def __str__(self):
        return str(self.store)
