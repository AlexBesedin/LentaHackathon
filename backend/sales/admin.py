from django.contrib import admin
from .models import Sales, SalesRecord


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'sku',
        'fact',
    )
    search_fields = (
        'store',
        'sku',
        'fact',
    )
    list_filter = (
       'store',
       'sku',
       'fact',
    )


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'sales_type',
        'sales_units',
        'sales_units_promo',
        'sales_rub',
        'sales_run_promo',
    )
    search_fields = (
        'date',
        'sales_type',
        'sales_units',
        'sales_units_promo',
        'sales_rub',
        'sales_run_promo',
    )
    list_filter = (
        'date',
        'sales_type',
        'sales_units',
        'sales_units_promo',
        'sales_rub',
        'sales_run_promo',
    )

