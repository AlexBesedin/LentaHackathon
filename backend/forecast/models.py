from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from stores.models import Store
from categories.models import Category


class StoreForecast(models.Model):
    store = models.ForeignKey(
        Store, 
        on_delete=models.CASCADE, 
        related_name='forecasts')
    forecast_date = models.DateField()
    
    def clean(self):
        super().clean()
        if self.forecast_date < timezone.now().date():
            raise ValidationError(
                {"forecast_date": "Дата прогноза не может быть в прошлом."}
                )

    def __str__(self):
        return f"{self.store.store_id} - {self.forecast_date}"


class SkuForecast(models.Model):
    forecast = models.ForeignKey(
        StoreForecast, 
        on_delete=models.CASCADE, 
        related_name='sku_forecasts'
        )
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sku_forecasts'
        )


class DailySalesForecast(models.Model):
    sales_units = models.ForeignKey(
        SkuForecast, 
        on_delete=models.CASCADE)
    date = models.DateField()
    target = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.sku_forecast} - {self.sku_forecast.sku} - {self.date} - {self.target}"