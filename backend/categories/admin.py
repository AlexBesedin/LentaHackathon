from categories.models import Category
from django.conf import settings
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'group',
        'category',
        'subcategory',
        'uom',
    )
    search_fields = (
        'sku',
        'group',
        'category',
        'subcategory',
        'uom',
    )
    list_filter = (
        'sku',
        'group',
        'category',
        'subcategory',
        'uom',
    )
    ordering = ('sku',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


admin.site.register(Category, CategoryAdmin)
