from django.db import models


class Stores(models.Model):
    """Класс магазинов."""

    store = models.CharField(
        max_length=50,
        verbose_name='захэшированное id магазина',
    )

    class Meta:
        ordering = ('store',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.store


class City(models.Model):
    """Класс городов магазинов."""

    city = models.CharField(
        max_length=50,
        verbose_name='захэшированное id города',
    )

    class Meta:
        ordering = ('city',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city


class Division(models.Model):
    """Класс отделов магазинов."""

    division = models.CharField(
        max_length=50,
        verbose_name='захэшированное id дивизиона',
    )

    class Meta:
        ordering = ('division',)
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.division


class Type_format(models.Model):
    """Класс магазинов."""

    type_format = models.IntegerField(
        verbose_name='id формата магазина',
    )

    class Meta:
        ordering = ('type_format',)
        verbose_name = 'Формат магазины'
        verbose_name_plural = 'Форматы магазинов'

    def __str__(self):
        return self.type_format


class Location(models.Model):
    """Класс локации магазинов."""

    loc = models.IntegerField(
        verbose_name='id тип локации/окружения магазина',
    )

    class Meta:
        ordering = ('loc',)
        verbose_name = 'Тип локации магазины'
        verbose_name_plural = 'Типы локаций магазинов'

    def __str__(self):
        return self.loc


class Size(models.Model):
    """Типы размеров магазинов."""

    size = models.IntegerField(
        verbose_name='id типа размера магазина',
    )

    class Meta:
        ordering = ('size',)
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.size


class Store(models.Model):
    """Класс магазинов продуктовой иерархии."""

    store = models.ForeignKey(
        Stores,
        on_delete=models.CASCADE,
        related_name='stores'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='cities'
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='divisions'
    )
    type_format = models.ForeignKey(
        Type_format,
        on_delete=models.CASCADE,
        related_name='type_formats'
    )
    loc = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='locs'
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
