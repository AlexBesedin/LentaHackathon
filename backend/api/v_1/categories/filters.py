import django_filters
from categories.models import Category


class CategoryFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter(field_name="sku")
    group = django_filters.CharFilter(field_name="group__group")
    category = django_filters.CharFilter(field_name="category__category")
    subcategory = django_filters.CharFilter(field_name="subcategory__subcategory")
    uom = django_filters.CharFilter(field_name="uom")

    class Meta:
        model = Category
        fields = ['sku', 'group', 'category', 'subcategory', 'uom']