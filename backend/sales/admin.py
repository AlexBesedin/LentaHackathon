from django.contrib import admin
from .models import Sales, SalesRecord


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['store', 'sku']
    search_fields = ['store__store', 'sku__sku']


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = [
        'fact', 
        'date', 
        'sales_type', 
        'sales_units', 
        'sales_units_promo', 
        'sales_rub', 
        'sales_rub_promo'
        ]
    search_fields = [
        'fact__store__store', 
        'fact__sku__sku', 
        'date'
        ]
    list_filter = ['sales_type', 'date']
