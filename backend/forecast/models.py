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
        verbose_name='Магазин'
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
        return f"{self.store.store_id} - {self.forecast_date}"


class SkuForecast(models.Model):
    """Модель прогноза товара"""
    
    forecast = models.ForeignKey(
        StoreForecast, 
        on_delete=models.CASCADE, 
        related_name='sku_forecasts',
        verbose_name='Прогноз магазина'
        )
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sku_forecasts',
        verbose_name='Товар'
        )

    class Meta:
        verbose_name = 'Прогноз товара'
        verbose_name_plural = 'Прогнозы товаров'


class DailySalesForecast(models.Model):
    """Модель ежедневного прогноза продаж"""
    sales_units = models.ForeignKey(
        SkuForecast, 
        on_delete=models.CASCADE,
        verbose_name='Прогноз товара'
        )
    date = models.DateField(
        verbose_name='Дата'
        )
    target = models.PositiveIntegerField(
        verbose_name='Цель'
        )
    
    class Meta:
        verbose_name = 'Ежедневный прогноз продаж'
        verbose_name_plural = 'Ежедневные прогнозы продаж'
    

    def __str__(self):
        return f"{self.sku_forecast} - {self.sku_forecast.sku} - {self.date} - {self.target}"
