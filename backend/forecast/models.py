from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Forecast(models.Model):
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


class SalesUnitForecast(models.Model):
    forecast = models.ForeignKey(
        Forecast, 
        on_delete=models.CASCADE, 
        related_name='sales_units_forecasts')
    sku = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='sales_units_sku'
        )
    date = models.DateField()
    target = models.IntegerField()
    
    
    def clean(self):
        super().clean()
        if self.target < 0:
            raise ValidationError(
                {"target": "Target должно быть целым положительным числом."}
                )
        if self.date < timezone.now().date():
            raise ValidationError(
                {"date": "Дата не может относиться к прошлому."}
                )
    
    class Meta:
        unique_together = ['forecast', 'sku']

    def __str__(self):
        return f"{self.forecast} - {self.sku.sku} - {self.date} - {self.target}"
