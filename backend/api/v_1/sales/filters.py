from django_filters import rest_framework as filters
from sales.models import Sales


class SalesFilter(filters.FilterSet):
    store = filters.CharFilter(field_name="store__store")
    sku = filters.CharFilter(field_name="sku__sku")
    date = filters.DateFilter(field_name="fact__date")
    date_from = filters.DateFilter(field_name="fact__date", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="fact__date", lookup_expr='lte')
    sales_type = filters.NumberFilter(field_name="fact__sales_type")
    sales_units = filters.NumberFilter(field_name="fact__sales_units")
    sales_units_promo = filters.NumberFilter(field_name="fact__sales_units_promo")
    sales_rub = filters.NumberFilter(field_name="fact__sales_rub")
    sales_run_promo = filters.NumberFilter(field_name="fact__sales_run_promo")

    class Meta:
        model = Sales
        fields = [
            'store', 
            'sku', 
            'date', 
            'date_from',
            'date_to',
            'sales_type', 
            'sales_units', 
            'sales_units_promo', 
            'sales_rub', 
            'sales_run_promo'
        ]