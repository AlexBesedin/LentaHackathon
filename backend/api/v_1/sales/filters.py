from decimal import Decimal

from dateutil.parser import parse
from rest_framework.filters import BaseFilterBackend

# from sales.models import Sales


class SaleFilterBackend(BaseFilterBackend):
    """
    Фильтр, который позволяет фильтровать данные по продажам на основе 
    - store (магазин)
    - sku (захэшированное id товара)
    - date (Дата(день))
    - sales_type (флаг наличия промо)
    - sales_units (число проданных товаров без признака промо)
    - sales_units_promo (число проданных товаров с признаком промо)
    - sales_rub (продажи без признака промо в РУБ)
    - sales_rub_promo (продажи с признаком промо в РУБ;)
    """

    def filter_queryset(self, request, queryset, view):

        store_param = request.query_params.get('store')
        sku_param = request.query_params.get('sku')
        date_param = request.query_params.get('date')
        sales_type_param = request.query_params.get('sales_type')
        sales_units_param = request.query_params.get('sales_units')
        sales_units_promo_param = request.query_params.get('sales_units_promo')
        sales_rub_param = request.query_params.get('sales_rub')
        sales_rub_promo_param = request.query_params.get('sales_rub_promo')

        if store_param is not None:
            store_list = store_param.split(",")
            queryset = queryset.filter(store__store__title__in=store_list)

        # Фильтр хэша товара предсказания
        if sku_param is not None:
            sku_list = sku_param.split(",")
            queryset = queryset.filter(sku__sku__in=sku_list)

        # Фильтр по дате
        if date_param is not None:
            from dateutil.parser import parse
            date_list = [parse(date_str).date() for date_str
                         in date_param.split(",")]
            queryset = queryset.filter(fact__date__in=date_list)

        # Фильтр по флаг наличия промо (sales_type)
        if sales_type_param is not None:
            sales_type_list = [int(x) for x in sales_type_param.split(",")]
            queryset = queryset.filter(fact__sales_type__in=sales_type_list)

        # Фильтр по числу проданных товаров без признака промо (sales_units)
        if sales_units_param is not None:
            sales_units_list = [int(x) for x in sales_units_param.split(",")]
            queryset = queryset.filter(fact__sales_units__in=sales_units_list)

        # Фильтр по числу проданных товаров с признаком промо
        # (sales_units_promo)
        if sales_units_promo_param is not None:
            sales_units_promo_list = [int(x) for x in
                                      sales_units_promo_param.split(",")]
            queryset = queryset.filter(
                fact__sales_units_promo__in=sales_units_promo_list)

        # Фильтр по продажам без признака промо в РУБ (sales_rub)
        if sales_rub_param is not None:
            sales_rub_list = [Decimal(x) for x in sales_rub_param.split(",")]
            queryset = queryset.filter(fact__sales_rub__in=sales_rub_list)

        # Фильтр по продажам с признаком промо в РУБ; (sales_rub_promo)
        if sales_rub_promo_param is not None:
            sales_rub_promo_list = [Decimal(x) for x in
                                    sales_rub_promo_param.split(",")]
            queryset = queryset.filter(
                fact__sales_rub_promo__in=sales_rub_promo_list)

        return queryset


# class SalesFilter(django_filters.FilterSet):
#     """Фильтр для общих продаж"""
#     store = django_filters.CharFilter(field_name='store__store__title', lookup_expr='exact')
#     group = django_filters.CharFilter(field_name='sku__group__group', lookup_expr='exact')
#     category = django_filters.CharFilter(field_name='sku__category__category', lookup_expr='exact')
#     uom = django_filters.CharFilter(method='filter_uom')

#     class Meta:
#         model = Sales
#         fields = ['store', 'group', 'category', 'uom']

#     def filter_uom(self, queryset, name, value):
#         uom_mapping = {'шт': 1, 'кг': 17}
#         value = uom_mapping.get(value.strip().lower(), value)
#         return queryset.filter(sku__uom=value)


class SalesDetailBackend(BaseFilterBackend):
    """Фильтр для общих продаж"""

    def filter_queryset(self, request, queryset, view):

        store_param = request.query_params.get('store')
        category_param = request.query_params.get('category')
        group_param = request.query_params.get('group')
        uom_param = request.query_params.get('uom')

        if store_param is not None:
            store_list = store_param.split(",")
            queryset = queryset.filter(store__store__title__in=store_list)

        if category_param is not None:
            category_list = category_param.split(",")
            queryset = queryset.filter(
                sku__category__category__in=category_list)

        if group_param is not None:
            group_list = group_param.split(",")
            queryset = queryset.filter(sku__group__group__in=group_list)

        if uom_param is not None:
            uom_mapping = {'шт': 1, 'кг': 17}
            uom_param = uom_mapping.get(uom_param.strip().lower(), uom_param)
            queryset = queryset.filter(sku__uom=uom_param)

        return queryset
