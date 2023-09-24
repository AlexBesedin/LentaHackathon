from django.contrib import admin
from .models import StoreForecast, SkuForecast, DailySalesForecast


@admin.register(StoreForecast)
class StoreForecastAdmin(admin.ModelAdmin):
    list_display = ['store', 'forecast_date']
    search_fields = ['store__store_id', 'forecast_date']
    list_filter = ['forecast_date']


@admin.register(SkuForecast)
class SkuForecastAdmin(admin.ModelAdmin):
    list_display = ['forecast', 'sku']
    search_fields = ['forecast__store__store_id', 'sku__sku']
    list_filter = ['forecast']


@admin.register(DailySalesForecast)
class DailySalesForecastAdmin(admin.ModelAdmin):
    list_display = ['sales_units', 'date', 'target']
    search_fields = [
        'sales_units__forecast__store__store_id', 
        'sales_units__sku__sku', 
        'date']
    list_filter = ['date', 'sales_units']
