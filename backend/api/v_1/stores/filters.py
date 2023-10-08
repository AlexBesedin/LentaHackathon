from django_filters import (AllValuesMultipleFilter, BooleanFilter, CharFilter,
                            ChoiceFilter, FilterSet, NumberFilter,)

from stores.models import Store


class StoreFilter(FilterSet):
    store_exact = AllValuesMultipleFilter(field_name='store__title', label='Точное название магазина')
    store_contains = CharFilter(field_name='store__title', lookup_expr='icontains', label='Содержит в названии магазина')
    city_exact = AllValuesMultipleFilter(field_name="city", label='Точный город')
    city_contains = CharFilter(field_name='city', lookup_expr='icontains', label='Содержит в названии города')
    division = AllValuesMultipleFilter(field_name="division", label='Дивизион')
    type_format = AllValuesMultipleFilter(field_name="type_format", label='Тип формата')
    loc = AllValuesMultipleFilter(field_name="loc", label='Местоположение')
    size = NumberFilter(field_name="size", label='Размер')
    is_active = BooleanFilter(label='Статус активности')

    class Meta:
        model = Store
        fields = [
            'store_exact', 
            'store_contains', 
            'city_exact', 
            'city_contains', 
            'division', 
            'type_format', 
            'loc', 
            'size', 
            'is_active'
        ]

