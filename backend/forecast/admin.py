from django.contrib import admin
from .models import StoreForecast, DailySalesForecast


@admin.register(StoreForecast)
class StoreForecastAdmin(admin.ModelAdmin):
    list_display = ('store', 'sku', 'forecast_date',)
    search_fields = ('store__name', 'sku__name',)
    list_filter = ('forecast_date', 'store',)
    
    # def has_add_permission(self, request):
    #     return False


@admin.register(DailySalesForecast)
class DailySalesForecastAdmin(admin.ModelAdmin):
    list_display = ('forecast_sku_id', 'date', 'target',)
    search_fields = ('forecast_sku_id__store__name', 'forecast_sku_id__sku__name',)
    list_filter = ('date', 'forecast_sku_id',)
    
    # def has_add_permission(self, request):
    #     return False
