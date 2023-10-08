import django_filters

from categories.models import Category


class CategoryFilter(django_filters.FilterSet):
    """Фильтр для категорий."""

    sku = django_filters.CharFilter(
        lookup_expr='icontains'
        )
    group = django_filters.AllValuesMultipleFilter(
        field_name='group__group'
        )
    category = django_filters.AllValuesMultipleFilter(
        field_name='category__category'
        )
    subcategory = django_filters.AllValuesMultipleFilter(
        field_name='subcategory__subcategory'
        )
    uom = django_filters.NumberFilter()

    class Meta:
        model = Category
        fields = [
            'sku',
            'group__group',
            'category__category',
            'subcategory__subcategory',
        ]
