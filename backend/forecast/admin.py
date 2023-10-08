from django.contrib import admin

from .models import DailySalesForecast, StoreForecast, UserBookmark


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

  
@admin.register(UserBookmark)   
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_forecast', 'created_at')
    search_fields = ('user__username', 'store_forecast__store__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
