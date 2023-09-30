from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from stores.models import Store
from categories.models import Category


class StoreForecast(models.Model):
    """Модель данных предсказаний"""
    
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE, 
        related_name='forecasts',
        verbose_name='захэшированное id магазина'
        )
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sku_forecasts',
        verbose_name='захэшированное id товара'
        )
    
    forecast_date = models.DateField(
        verbose_name='Дата прогноза'
        )
    
    def clean(self):
        super().clean()
        if self.forecast_date < timezone.now().date():
            raise ValidationError(
                {"forecast_date": "Дата прогноза не может быть в прошлом."}
                )

    class Meta:
        verbose_name = 'Прогноз магазина'
        verbose_name_plural = 'Прогнозы магазинов'

    def __str__(self):
        return f"{self.store} - {self.forecast_date}"



class DailySalesForecast(models.Model):
    """Модель ежедневного прогноза продаж"""
    forecast_sku_id  = models.ForeignKey(
        StoreForecast, 
        on_delete=models.CASCADE,
        related_name='sales_units',
        verbose_name='Прогноз товара'
        )
    date = models.DateField(
        verbose_name='Дата(день)'
        )
    target = models.PositiveIntegerField(
        verbose_name='спрос в ШТ.'
        )
    
    class Meta:
        verbose_name = 'Ежедневный прогноз продаж'
        verbose_name_plural = 'Ежедневные прогнозы продаж'
    

    def __str__(self):
        return f"{self.forecast_sku_id} - {self.forecast_sku_id.sku} - {self.date} - {self.target}"
