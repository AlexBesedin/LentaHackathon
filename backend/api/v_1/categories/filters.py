import django_filters
from django_filters import rest_framework as filters

from categories.models import Category, Group, CategoryProduct, Subcategory


class CategoryFilter(django_filters.FilterSet):
    sku = filters.CharFilter(lookup_expr='icontains')
    group = django_filters.ModelMultipleChoiceFilter(
        queryset=Group.objects.all(), 
        to_field_name='group', 
        field_name='group__group'
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=CategoryProduct.objects.all(), 
        to_field_name='category', 
        field_name='category__category'
    )
    subcategory = django_filters.ModelMultipleChoiceFilter(
        queryset=Subcategory.objects.all(), 
        to_field_name='subcategory', 
        field_name='subcategory__subcategory'
    )
    uom = filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = [
            'sku', 
            'group__group', 
            'category__category', 
            'subcategory__subcategory'
        ]