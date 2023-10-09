from django.conf import settings
from django.contrib import admin

from categories.models import Category, CategoryProduct, Group, Subcategory


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'group',
    )
    search_fields = (
        'group',
    )
    list_filter = (
        'group',
    )
    ordering = ('group',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'category',
    )
    search_fields = (
        'group',
        'category',
    )
    list_filter = (
        'group',
        'category',
    )
    ordering = ('category',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'subcategory',
        'category',
    )
    search_fields = (
        'subcategory',
        'category',
    )
    list_filter = (
        'subcategory',
        'category',
    )
    ordering = ('subcategory',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


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
admin.site.register(Group, GroupAdmin)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
