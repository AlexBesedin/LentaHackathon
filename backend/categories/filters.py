import django_filters
from categories.models import Category


class CategoryFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter(field_name="sku")
    group = django_filters.NumberFilter(field_name="group__id")
    category = django_filters.NumberFilter(field_name="category__id")
    subcategory = django_filters.NumberFilter(field_name="subcategory__id")

    class Meta:
        model = Category
        fields = ['sku', 'group', 'category', 'subcategory']