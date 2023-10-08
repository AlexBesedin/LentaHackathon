from categories.models import Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from stores.models import Store


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
    

class UserBookmark(models.Model):
    """Модель закладок пользователя для сохранения прогнозов."""
    
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='bookmarks',
        verbose_name='Пользователь'
        )
    store_forecast = models.ForeignKey(
        StoreForecast, 
        on_delete=models.CASCADE, 
        related_name='bookmarked_by',
        verbose_name='Прогноз магазина'
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
        )
    
    class Meta:
        verbose_name = 'Закладка прогнозов пользователя'
        verbose_name_plural = 'Закладки прогнозов пользователей'
        unique_together = [['user', 'store_forecast']]

    def __str__(self):
        return f"{self.user} - {self.store_forecast}"

